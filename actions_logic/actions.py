from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple
import random

import game_map.color as color
import utility_files.exceptions as exceptions

if TYPE_CHECKING:
    from game_logic.engine import Engine
    from entity.entity import Actor, Entity, Item, Chest
    from components.damageinfo import DamageInfo
    #from components.status import confusion_direction


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


class RangedAction(ActionWithDirection):
    def perform(self) -> None:
        # If dx/dy is different than 0, it has a target
        if self.dx == 0 and self.dy == 0:
            self.engine.message_log.add_message(f"You hear the {self.entity.equipment.ranged.equippable.projectile_name} hit a wall in the distance.")
        else:
            target = self.target_actor

            attack_desc = f"You hit the {target.name} with your {self.entity.equipment.ranged.equippable.projectile_name}"

            damage_modificator = target.damage_info.calculate_damage(self.entity.equipment.meelee.equippable.damage_type)
            damage = self.entity.fighter.power_ranged - target.fighter.defense
            
            # Calculate the damage to inflict to the target and elemental resistance/vulnerability
            if damage > 0 and damage_modificator > 0:    
                self.engine.message_log.add_message(f"{attack_desc} for {self.entity.fighter.power_ranged} damage!", color.player_atk)
                target.fighter.hp -= damage * damage_modificator
            else:
                self.engine.message_log.add_message(f"{attack_desc} but does no damage.", color.player_atk)
                if damage_modificator == 0:
                    self.engine.message_log.add_message(f"The {target.name} is immune.", color.player_atk)

            # This checks if the player is grabbed and the enemy is dead, and then release the player from the grabbed condition
            if self.entity == self.engine.player and self.entity.status.check_grabbed_condition and (damage > 0 and damage_modificator > 0):
                if (target.fighter.hp <= 0 or not target.is_alive) and target.status.dict_condition_attack["grab"]:
                    self.entity.status.dict_condition_afflicted["grab"] = False
                    self.engine.message_log.add_message(f"You are free from the grab.", color.player_atk)

            # After the damage, there is the check for the conditions effect.
            self.entity.status.affect_new_status(self, target, color.player_atk)


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")

        damage = self.entity.fighter.power_meelee - target.fighter.defense
        
        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        # Check if the entity is the player or the enemy to calculate the type of damage        
        if self.entity == self.engine.player:
            damage_modificator = target.damage_info.calculate_damage(self.entity.equipment.meelee.equippable.damage_type)
        else:
            damage_modificator = target.damage_info.calculate_damage(self.entity.damage_info.attack_type_return())

        #if the entity has fear status, it calculate a random chance to hit the opponent
        if self.entity.status.dict_condition_afflicted["fear"] or self.entity.status.dict_condition_afflicted["blindness"]:
            chance_to_hit = random.randint(1, 100)
        else:
            chance_to_hit = 100

        # Calculate the damage to inflict to the target and elemental resistance/vulnerability
        if damage > 0 and damage_modificator > 0 and chance_to_hit > 70:
            self.engine.message_log.add_message(f"{attack_desc} for {damage * damage_modificator} hit points.", attack_color)
            if damage_modificator == 2:
                self.engine.message_log.add_message(f"The damage is critical!", attack_color)
            elif damage_modificator == 0.5:
                self.engine.message_log.add_message(f"The damage is resisted!", attack_color)
            target.fighter.hp -= damage * damage_modificator
        else:
            if chance_to_hit > 70:
                self.engine.message_log.add_message(f"{attack_desc} but does no damage.", attack_color)
                if damage_modificator == 0:
                    self.engine.message_log.add_message(f"The {target.name} is immune.", attack_color)
            elif self.entity.status.dict_condition_afflicted["fear"]:
                self.engine.message_log.add_message(f"The {self.entity.name} missed as the fear blocked his attack.", attack_color)
            elif self.entity.status.dict_condition_afflicted["blindness"]:
                self.engine.message_log.add_message(f"The {self.entity.name} missed as it's unable to see.", attack_color)

        
        # This checks if the player is grabbed and the enemy is dead, and then release the player from the grabbed condition
        if self.entity == self.engine.player and self.entity.status.check_grabbed_condition and (damage > 0 and damage_modificator > 0):
            if (target.fighter.hp <= 0 or not target.is_alive) and target.status.dict_condition_attack["grab"]:
                self.entity.status.dict_condition_afflicted["grab"] = False
                self.engine.message_log.add_message(f"You are free from the grab.", attack_color)

        # After the damage, there is the check for the conditions effect.
        # This checks if the entity is an enemy or the player.
        self.entity.status.affect_new_status(self, target, attack_color)


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
            self.entity.status.dict_turns_passed["bleed"] = 0
        
        # Check for the poison turns
        elif self.entity.status.check_turns_poison:
            self.entity.status.effect_hp_damage()
            self.entity.status.dict_turns_passed["poison"] = 0

        # Check if the player is afflicted by confusion
        elif self.entity.status.dict_condition_afflicted["confusion"]:

            # If the number of turns is over the number of turns required for the confusion, end the confusion effect, reset the turns counter and let the player do his action
            if self.entity.status.check_turns_confusion:
                self.entity.status.dict_condition_afflicted["confusion"] = False
                if self.entity == self.engine.player:
                    self.engine.message_log.add_message(f"You are no longer confused!")
                else:
                    self.engine.message_log.add_message(f"The {self.entity.name} is no longer confused.")
            # Else, it creates a random direction and return the action for the random direction
            else:
                self.entity.status.dict_turns_passed["confusion"] += 1
                direction_x, direction_y = random.choice(
                    [
                        (-1, -1),  # Northwest
                        (0, -1),  # North
                        (1, -1),  # Northeast
                        (-1, 0),  # West
                        (1, 0),  # East
                        (-1, 1),  # Southwest
                        (0, 1),  # South
                        (1, 1),  # Southeast
                    ]
                )
                # Then check if there are actors or chests at the random direction
                if self.engine.game_map.get_actor_at_location(self.dx + direction_x, self.dy + direction_y):
                    return MeleeAction(self.entity, direction_x, direction_y).perform()
                elif self.engine.game_map.get_chest_at_location(self.dx + direction_x, self.dy + direction_y) and self.entity == self.engine.player:
                    return ChestAction(self.entity, direction_x, direction_y).perform()
                else:
                    return MovementAction(self.entity, direction_x, direction_y).perform()

        # Check if the player is afflicted by stun
        elif self.entity.status.dict_condition_afflicted["stun"]:
            # If the number of turns is over the number of turns required for the stun, end the stun effect, reset the turns counter and let the player do his action
            if self.entity.status.check_turns_stun:
                self.entity.status.dict_condition_afflicted["stun"] = False
                if self.entity == self.engine.player:
                    self.engine.message_log.add_message(f"You are no longer stunned!")
                else:
                    self.engine.message_log.add_message(f"The {self.entity.name} are no longer stunned!")
            # Else, it does the wait action for a turn
            else:
                self.entity.status.dict_turns_passed["stun"] += 1
                if self.entity == self.engine.player:
                    self.engine.message_log.add_message(f"You are stunned!")
                else:
                    self.engine.message_log.add_message(f"The {self.entity.name} is stunned and can't move!")
                return WaitAction(self.entity)
        
        # Check if the player is afflicted by condemnation
        elif self.entity.status.dict_condition_afflicted["condemnation"]:

            # If the number of turns is over the number of turns required for the condemnation, if is the player, the game is over
            if self.entity.status.check_turns_condemnation:
                if self.entity == self.engine.player:
                    self.engine.message_log.add_message(f"The weight of your condemnation reaches you!")
                else:
                    self.engine.message_log.add_message(f"The weight of your condemnation reaches the {self.entity.name}!")
                self.entity.fighter.hp = 0
            # Else, it adds a turns for the condemnation
            else:
                self.entity.status.dict_turns_passed["condemnation"] += 1
                self.engine.message_log.add_message(f"Death is soon approaching!")
                
        # Check if the player is afflicted by petrification
        elif self.entity.status.dict_condition_afflicted["petrification"]:

            # If the number of turns is over the number of turns required for the petrification, if is the player, the game is over
            if self.entity.status.check_turns_petrification:
                if self.entity == self.engine.player:
                    self.engine.message_log.add_message(f"All your body is now turned to stone!")
                else:
                    self.engine.message_log.add_message(f"All of {self.entity.name} body is now turned to stone!")
                self.entity.fighter.hp = 0
            # Else, it adds a turns for the petrification
            else:
                self.entity.status.dict_turns_passed["petrification"] += 1
                self.engine.message_log.add_message(f"More of your body is turning to stone!")
        
        # Check if the player is afflicted by blindness
        elif self.entity.status.dict_condition_afflicted["blindness"] and self.entity is not self.engine.player:
            direction_x, direction_y = random.choice(
                [
                    (-1, -1),  # Northwest
                    (0, -1),  # North
                    (1, -1),  # Northeast
                    (-1, 0),  # West
                    (1, 0),  # East
                    (-1, 1),  # Southwest
                    (0, 1),  # South
                    (1, 1),  # Southeast
                ]
            )
            # Then check if there are actors or chests at the random direction
            if self.engine.game_map.get_actor_at_location(self.dx + direction_x, self.dy + direction_y):
                return MeleeAction(self.entity, direction_x, direction_y).perform()
            elif self.engine.game_map.get_chest_at_location(self.dx + direction_x, self.dy + direction_y) and self.entity == self.engine.player:
                return ChestAction(self.entity, direction_x, direction_y).perform()
            else:
                return MovementAction(self.entity, direction_x, direction_y).perform()


        # After all the status, checks for the target actors or chests
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        elif self.target_chest and self.entity == self.engine.player:
            return ChestAction(self.entity, self.dx, self.dy).perform()
        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()
