from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple

import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item, Chest


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class PickupAction(Action):
    """Pickup an item and add it to the inventory, if there is room for it."""

    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Your inventory is full.")

                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.message_log.add_message(f"You picked up the {item.name}!")
                return

        raise exceptions.Impossible("There is nothing here to pick up.")


class ItemAction(Action):
    def __init__(self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        """Invoke the items ability, this action will be given to provide context."""
        if self.item.consumable:
            self.item.consumable.activate(self)


class DropItem(ItemAction):
    def perform(self) -> None:
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)

        self.entity.inventory.drop(self.item)


class EquipAction(Action):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity)

        self.item = item

    def perform(self) -> None:
        self.entity.equipment.toggle_equip(self.item)


class WaitAction(Action):
    def perform(self) -> None:
        pass


class TakeStairsAction(Action):
    def perform(self) -> None:
        """
        Take the stairs, if any exist at the entity's location.
        """
        if (self.entity.x, self.entity.y) == self.engine.game_map.downstairs_location:
            self.engine.game_world.generate_floor()
            self.engine.message_log.add_message("You descend the staircase.", color.descend)
        else:
            raise exceptions.Impossible("There are no stairs here.")


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        """Return the actor at this actions destination."""
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)
    
    @property
    def target_chest(self) -> Optional[Chest]:
        """Return the chest at this action destination."""
        return self.engine.game_map.get_chest_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")

        damage = self.entity.fighter.power - target.fighter.defense

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(f"{attack_desc} for {damage} hit points.", attack_color)
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(f"{attack_desc} but does no damage.", attack_color)        

        """This checks if the entity is an enemy or the player."""
        if self.entity.equipment.weapon is None and self.entity.equipment.accessory_1 is None and self.entity.equipment.accessory_2 is None:
            if self.entity.status.dict_condition_attack["attack_bleed"] == True:
                if target.status.dict_condition_afflicted["flag_bleed"] == False:
                    if not target.status.check_bleed_immunity:
                        target.status.dict_condition_afflicted["flag_bleed"] = True
                        self.engine.message_log.add_message(f"The {target.name} is bleeding!", attack_color)
                    else:
                        self.engine.message_log.add_message(f"The {target.name} is resistant to bleeding!", attack_color)
            if self.entity.status.dict_condition_attack["attack_poison"] == True:
                if target.status.dict_condition_afflicted["flag_poison"] == False:
                    if not target.status.check_poison_immunity:
                        target.status.dict_condition_afflicted["flag_poison"] = True
                        self.engine.message_log.add_message(f"The {target.name} is poisoned!", attack_color)
                    else:
                        self.engine.message_log.add_message(f"The {target.name} is resistant to poison!", attack_color)
                else:
                    self.engine.message_log.add_message(f"The {target.name} is already poisoned!", attack_color)

        else:
            """If the equipment of the player can create the status, it will check the other condition. 
               Then, it will check if the monster is already afflicted by the condition or if it's immune to the condition."""
            if (self.entity.equipment.weapon.equippable.status_effect == "bleed" or (self.entity.equipment.accessory_1 is not None and self.entity.equipment.accessory_1.equippable.status_effect == "bleed")):
                if target.status.dict_condition_afflicted["flag_bleed"] == False:
                    if not target.status.check_bleed_immunity:
                        target.status.dict_condition_afflicted["flag_bleed"] = True
                        self.engine.message_log.add_message(f"The {target.name} is bleeding!", attack_color)
                    else:
                        self.engine.message_log.add_message(f"The {target.name} is resistant to bleeding!", attack_color)
                else:
                    self.engine.message_log.add_message(f"The {target.name} is already bleeding!", attack_color)
            if (self.entity.equipment.weapon.equippable.status_effect == "poison" or (self.entity.equipment.accessory_1 is not None and self.entity.equipment.accessory_1.equippable.status_effect == "poison")):
                if target.status.dict_condition_afflicted["flag_poison"] == False:
                    if not target.status.check_poison_immunity:
                        target.status.dict_condition_afflicted["flag_poison"] = True
                        self.engine.message_log.add_message(f"The {target.name} is poisoned!", attack_color)
                    else:
                        self.engine.message_log.add_message(f"The {target.name} is resistant to poison!", attack_color)
                else:
                    self.engine.message_log.add_message(f"The {target.name} is already poisoned!", attack_color)


class ChestAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_chest
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for chest in self.engine.game_map.chests:
            if target == chest:
                if target.item != None:
                    if target.locked is False:
                        if len(inventory.items) >= inventory.capacity:
                            raise exceptions.Impossible("Your inventory is full.")

                        item = target.item
                        item.parent = self.entity.inventory
                        inventory.items.append(item)
                        target.item = None

                        self.engine.message_log.add_message(f"The locked chest contains {item.name}. You added it to your inventory.")
                        return
                    else:
                        raise exceptions.Impossible("The chest is locked.")
                else:
                    raise exceptions.Impossible("The chest is empty.")
            else:
                pass


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is blocked.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is blocked by a tile.
            raise exceptions.Impossible("That way is blocked.")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # Destination is blocked by an entity.
            raise exceptions.Impossible("That way is blocked.")

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        # Before any action is performed, check for all the different condition flags

        # Check for the bleed turns
        if self.entity.status.check_turns_bleed:
            self.entity.status.effect_hp_damage()
            self.entity.status.turns_passed = 0
        
        # Check for the poison turns
        elif self.entity.status.check_turns_poison:
            self.entity.status.effect_hp_damage()
            self.entity.status.turns_passed = 0

        # Check if the player is afflicted by confusion
        elif self.entity.status.dict_condition_afflicted["flag_confusion"] and self.entity == self.engine.player:
            # If the number of turns is minor than the max number of turns, it creates a random direction and return the action for the random direction
            if self.entity.status.check_turns_confusion:
                self.entity.status.turns_passed += 1
                direction_x, direction_y = self.entity.status.confusion_direction()
                # Then check if there are actors or chests at the random direction
                if self.engine.game_map.get_actor_at_location(self.x + direction_x, self.y + direction_y):
                    return MeleeAction(self.entity, direction_x, direction_y).perform()
                elif self.engine.game_map.get_chest_at_location(self.x + direction_x, self.y + direction_y):
                    return ChestAction(self.entity, direction_x, direction_y).perform()
                else:
                    return MovementAction(self.entity, direction_x, direction_y).perform()
            # Else, end the confusion effect and reset the turns
            else:
                self.entity.status.dict_condition_afflicted["flag_confusion"] = False
                self.entity.status.turns_passed = 0

        # Check if the player is afflicted by stun
        elif self.entity.status.dict_condition_afflicted["flag_stun"] and self.entity == self.engine.player:
            ""
            if self.entity.status.check_turns_stun:
                self.entity.status.dict_condition_afflicted["flag_stun"] = False
                self.entity.status.turns_passed = 0
            # Else, it does the wait action for a turn
            else:
                self.entity.status.turns_passed += 1
                return WaitAction(self.entity)
        else:
            self.entity.status.turns_passed += 1

        # After all the status, checks for the target actors or chests
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        elif self.target_chest and self.entity == self.engine.player:
            return ChestAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
