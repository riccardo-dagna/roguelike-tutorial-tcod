from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple

import game_map.color as color
import utility_files.exceptions as exceptions

if TYPE_CHECKING:
    from game_logic.engine import Engine
    from entity.entity import Actor, Entity, Item, Chest
    from components.damageinfo import DamageInfo
    from components.status import confusion_direction


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

        # Check if the entity is the player or the enemy to calculate the type of damage        
        if self.entity == self.engine.player:
            damage_modificator = target.damage_info.calculate_damage(self.entity.equipment.weapon.equippable.damage_type)
        else:
            damage_modificator = target.damage_info.calculate_damage(self.entity.damage_info.attack_type_return())

        # Calculate the damage to inflict to the target and elemental resistance/vulnerability
        if damage > 0 and damage_modificator > 0:
            self.engine.message_log.add_message(f"{attack_desc} for {damage * damage_modificator} hit points.", attack_color)
            if damage_modificator == 2:
                self.engine.message_log.add_message(f"The damage is critical!", attack_color)
            elif damage_modificator == 0.5:
                self.engine.message_log.add_message(f"The damage is resisted!", attack_color)
            target.fighter.hp -= damage * damage_modificator
        else:
            self.engine.message_log.add_message(f"{attack_desc} but does no damage.", attack_color)
            if damage_modificator == 0:
                self.engine.message_log.add_message(f"The {target.name} is immune.", attack_color)
        
        # This checks if the player is grabbed and the enemy is dead, and then release the player from the grabbed grabbed condition
        if self.entity == self.engine.player and self.entity.status.check_grabbed_condition:
            if (target.fighter.hp <= 0 or not target.is_alive) and target.status.dict_condition_attack["attack_grab"]:
                self.entity.status.dict_condition_afflicted["flag_grab"] = False
                self.engine.message_log.add_message(f"You are free from the grab.", attack_color)

        # After the damage, there is the check for the conditions effect.
        # This checks if the entity is an enemy or the player.
        # affect_new_status(self, target)
        if self.entity.equipment.weapon is None and self.entity.equipment.accessory_1 is None and self.entity.equipment.accessory_2 is None:
            """ If the enemy can affect the player with a condition from an attack, it will not check the other condition. 
               Then, it will check if the player is already afflicted by the condition or if it's immune to the condition."""
            if self.entity.status.dict_condition_attack["attack_bleed"]:
                if not target.status.dict_condition_afflicted["flag_bleed"]:
                    if not target.status.check_bleed_immunity:
                        target.status.dict_condition_afflicted["flag_bleed"] = True
                        self.engine.message_log.add_message(f"The {target.name} is bleeding!", attack_color)
                    else:
                        self.engine.message_log.add_message(f"The {target.name} is resistant to bleeding!", attack_color)
                else:
                    self.engine.message_log.add_message(f"The {target.name} is already bleeding!", attack_color)
            if self.entity.status.dict_condition_attack["attack_poison"]:
                if not target.status.dict_condition_afflicted["flag_poison"]:
                    if not target.status.check_poison_immunity:
                        target.status.dict_condition_afflicted["flag_poison"] = True
                        self.engine.message_log.add_message(f"The {target.name} is poisoned!", attack_color)
                    else:
                        self.engine.message_log.add_message(f"The {target.name} is resistant to poison!", attack_color)
                else:
                    self.engine.message_log.add_message(f"The {target.name} is already poisoned!", attack_color)
            if self.entity.status.dict_condition_attack["attack_stun"]:
                if not target.status.dict_condition_afflicted["flag_stun"]:
                    if not target.status.check_stun_immunity:
                        target.status.dict_condition_afflicted["flag_stun"] = True
                        target.status.turns_passed = 0
                        self.engine.message_log.add_message(f"The {target.name} is stunned!", attack_color)
                    else:
                        self.engine.message_log.add_message(f"The {target.name} is resistant to stun!", attack_color)
                else:
                    self.engine.message_log.add_message(f"The {target.name} is already stunned!", attack_color)
            if self.entity.status.dict_condition_attack["attack_confusion"]:
                if not target.status.dict_condition_afflicted["flag_confusion"]:
                    if not target.status.check_confusion_immunity:
                        target.status.dict_condition_afflicted["flag_confusion"] = True
                        target.status.turns_passed = 0
                        self.engine.message_log.add_message(f"The {target.name} is confusion!", attack_color)
                    else:
                        self.engine.message_log.add_message(f"The {target.name} is resistant to confusion!", attack_color)
                else:
                    self.engine.message_log.add_message(f"The {target.name} is already confusion!", attack_color)
            if self.entity.status.dict_condition_attack["attack_grab"]:
                if not target.status.check_grabbed_condition:
                    if not target.status.check_grab_immunity:
                        target.status.dict_condition_afflicted["flag_grab"] = True
                        target.status.turns_passed = 0
                        self.engine.message_log.add_message(f"The {target.name} is grabbed by the {self.entity.name}!", attack_color)
                    else:
                        self.engine.message_log.add_message(f"The {target.name} is too agile to be grabbed!", attack_color)
                else:
                    self.engine.message_log.add_message(f"The {target.name} is already grabbed by {self.entity.name}!", attack_color)



        else:
            """Check if the equipment of the player can create the conditions specified. 
               Then, it will check if the monster is already afflicted by the condition or if it's immune to the condition."""
            if (self.entity.equipment.weapon.equippable.status_effect == "bleed" or (self.entity.equipment.accessory_1 is not None and self.entity.equipment.accessory_1.equippable.status_effect == "bleed")):
                if not target.status.dict_condition_afflicted["flag_bleed"]:
                    if not target.status.check_bleed_immunity:
                        target.status.dict_condition_afflicted["flag_bleed"] = True
                        self.engine.message_log.add_message(f"The {target.name} is bleeding!", attack_color)
                    else:
                        self.engine.message_log.add_message(f"The {target.name} is resistant to bleeding!", attack_color)
                else:
                    self.engine.message_log.add_message(f"The {target.name} is already bleeding!", attack_color)
            if (self.entity.equipment.weapon.equippable.status_effect == "poison" or (self.entity.equipment.accessory_1 is not None and self.entity.equipment.accessory_1.equippable.status_effect == "poison")):
                if not target.status.dict_condition_afflicted["flag_poison"]:
                    if not target.status.check_poison_immunity:
                        target.status.dict_condition_afflicted["flag_poison"] = True
                        self.engine.message_log.add_message(f"The {target.name} is poisoned!", attack_color)
                    else:
                        self.engine.message_log.add_message(f"The {target.name} is resistant to poison!", attack_color)
                else:
                    self.engine.message_log.add_message(f"The {target.name} is already poisoned!", attack_color)
            if (self.entity.equipment.weapon.equippable.status_effect == "stun" or (self.entity.equipment.accessory_1 is not None and self.entity.equipment.accessory_1.equippable.status_effect == "stun")):
                if not target.status.dict_condition_afflicted["flag_stun"]:
                    if not target.status.check_stun_immunity:
                        target.status.dict_condition_afflicted["flag_stun"] = True
                        target.status.turns_passed = 0
                        self.engine.message_log.add_message(f"The {target.name} is stunned!", attack_color)
                    else:
                        self.engine.message_log.add_message(f"The {target.name} is resistant to stun!", attack_color)
                else:
                    self.engine.message_log.add_message(f"The {target.name} is already stunned!", attack_color)
            if (self.entity.equipment.weapon.equippable.status_effect == "confusion" or (self.entity.equipment.accessory_1 is not None and self.entity.equipment.accessory_1.equippable.status_effect == "confusion")):
                if not target.status.dict_condition_afflicted["flag_confusion"]:
                    if not target.status.check_confusion_immunity:
                        target.status.dict_condition_afflicted["flag_confusion"] = True
                        target.status.turns_passed = 0
                        self.engine.message_log.add_message(f"The {target.name} is confused!", attack_color)
                    else:
                        self.engine.message_log.add_message(f"The {target.name} is resistant to confusion!", attack_color)
                else:
                    self.engine.message_log.add_message(f"The {target.name} is already confusion!", attack_color)
            if (self.entity.equipment.weapon.equippable.status_effect == "grab" or (self.entity.equipment.accessory_1 is not None and self.entity.equipment.accessory_1.equippable.status_effect == "grab")):
                if not target.status.check_grabbed_condition:
                    if not target.status.check_grab_immunity:
                        target.status.dict_condition_afflicted["flag_grab"] = True
                        target.status.turns_passed = 0
                        self.engine.message_log.add_message(f"The {target.name} is grabbed by the {self.entity.name}!", attack_color)
                    else:
                        self.engine.message_log.add_message(f"The {target.name} is too agile to be grabbed!", attack_color)
                else:
                    self.engine.message_log.add_message(f"The {target.name} is already grabbed by the {self.entity.name}!", attack_color)


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
        if self.engine.game_map.get_chest_at_location(dest_x, dest_y) and self.entity != self.engine.player:
            # Destination is blocked by an chest for a non player.
            raise exceptions.Impossible("That way is blocked.")
        if self.entity.status.check_grabbed_condition:
            # The entity is grabbed and can't move.
            raise exceptions.Impossible("You are grabbed, you can't move.")

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
        elif self.entity.status.dict_condition_afflicted["flag_confusion"]:

            # If the number of turns is over the number of turns required for the confusion, end the confusion effect, reset the turns counter and let the player do his action
            if self.entity.status.check_turns_confusion:
                self.entity.status.dict_condition_afflicted["flag_confusion"] = False
                self.entity.status.turns_passed = 0
                if self.entity == self.engine.player:
                    self.engine.message_log.add_message(f"You are no longer confused!")
                else:
                    self.engine.message_log.add_message(f"The {self.entity.name} is no longer confused.")
            # Else, it creates a random direction and return the action for the random direction
            else:
                self.entity.status.turns_passed += 1
                direction_x, direction_y = confusion_direction()
                # Then check if there are actors or chests at the random direction
                if self.engine.game_map.get_actor_at_location(self.dx + direction_x, self.dy + direction_y):
                    return MeleeAction(self.entity, direction_x, direction_y).perform()
                elif self.engine.game_map.get_chest_at_location(self.dx + direction_x, self.dy + direction_y) and self.entity == self.engine.player:
                    return ChestAction(self.entity, direction_x, direction_y).perform()
                else:
                    return MovementAction(self.entity, direction_x, direction_y).perform()

        # Check if the player is afflicted by stun
        elif self.entity.status.dict_condition_afflicted["flag_stun"]:
            # If the number of turns is over the number of turns required for the stun, end the stun effect, reset the turns counter and let the player do his action
            if self.entity.status.check_turns_stun:
                self.entity.status.dict_condition_afflicted["flag_stun"] = False
                self.entity.status.turns_passed = 0
                if self.entity == self.engine.player:
                    self.engine.message_log.add_message(f"You are no longer stunned!")
                else:
                    self.engine.message_log.add_message(f"The {self.entity.name} are no longer stunned!")
            # Else, it does the wait action for a turn
            else:
                self.entity.status.turns_passed += 1
                if self.entity == self.engine.player:
                    self.engine.message_log.add_message(f"You are stunned!")
                else:
                    self.engine.message_log.add_message(f"The {self.entity.name} is stunned and can't move!")
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
