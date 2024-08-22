from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Tuple
import random

import numpy as np
import tcod

from actions_logic.actions import Action, BumpAction, MeleeAction, MovementAction, WaitAction, RangedAction, SpecialAttackAction
from entity.entity import Actor

if TYPE_CHECKING:
    from entity.entity import Actor
    from components.status import confusion_direction


class BaseAI(Action):
    def perform(self) -> None:
        raise NotImplementedError()

    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """Compute and return a path to the target position.

        If there is no valid path then returns an empty list.
        """
        # Copy the walkable array.
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            # Check that an enitiy blocks movement and the cost isn't zero (blocking.)
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # Add to the cost of a blocked position.
                # A lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths in
                # order to surround the player.
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y))  # Start position.

        # Compute the path to the destination and remove the starting point.
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]


#This AI is for normal enemy that attack meelee
class HostileMeeleeEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:        
        # If the entity is confused, it does a BumpAction with a random direction
        if self.entity.status.dict_condition_afflicted["confusion"]:
            return BumpAction(self.entity, 1, 1).perform()
        # If the entity is charmed, it attacks the closest actor (not the player) or it moves close to it, otherwise it waits
        # If the entity is enraged, it attacks the closest actor or it moves close to it, otherwise it waits 
        # If it's not both, it attacks the player or it moves close to it, otherwise it waits
        else:
            if not ((self.entity.status.check_turns_charm and self.entity.status.dict_condition_afflicted["charm"]) or (self.entity.status.check_turns_rage and self.entity.status.dict_condition_afflicted["rage"])) or (not self.entity.status.dict_condition_afflicted["charm"] and self.entity.status.dict_condition_afflicted["rage"]):
                
                #The target is chosen depending on the status
                if self.entity.status.dict_condition_afflicted["charm"]:
                    self.entity.status.dict_turns_passed["charm"] += 1
                    target = self.engine.game_map.get_closest_actor(self.entity, 15, False)
                elif self.entity.status.dict_condition_afflicted["rage"]:
                    self.entity.status.dict_turns_passed["rage"] += 1
                    target = self.engine.game_map.get_closest_actor(self.entity, 15, True)
                else:
                    target = self.engine.player
                    
                if target:
                    dx = target.x - self.entity.x
                    dy = target.y - self.entity.y
                    distance = max(abs(dx), abs(dy)) # Chebyshev distance.
                    if self.engine.game_map.visible[self.entity.x, self.entity.y]:
                        if distance <= 1:
                            return BumpAction(self.entity, dx, dy).perform()
                        
                        self.path = self.get_path_to(target.x, target.y)

                         # If the entity is not afraid, it moves in the direction of the player
                        if not self.entity.status.dict_condition_afflicted["fear"]:
                            # If the entity is not blind, it moves in the direction of the player
                            if not self.entity.status.dict_condition_afflicted["blindness"]:
                                if self.path:
                                    dest_x, dest_y = self.path.pop(0)
                                    return BumpAction(
                                        self.entity,
                                        dest_x - self.entity.x,
                                        dest_y - self.entity.y,
                                    ).perform()
                            #If the entity is blind, it moves in a random direction as the confusion status
                            else:
                                return BumpAction(self.entity, dx, dy).perform()
                            
                        # If the entity is afraid, it moves in the direction contrary of the player
                        else:
                            if self.path:
                                dest_x, dest_y = self.path.pop(0)
                                return BumpAction(
                                    self.entity,
                                    -(dest_x - self.entity.x),
                                    -(dest_y - self.entity.y),
                                ).perform()
            else:
                if self.entity.status.dict_condition_afflicted["charm"]:
                    self.engine.message_log.add_message(f"The {self.entity.name} is no longer charmed.")
                    self.entity.status.dict_turns_passed["charm"] = 0
                    self.entity.status.dict_condition_afflicted["charm"] = False
                elif self.entity.status.dict_condition_afflicted["rage"]:
                    self.engine.message_log.add_message(f"The {self.entity.name} is no longer enraged.")
                    self.entity.status.dict_turns_passed["rage"] = 0
                    self.entity.status.dict_condition_afflicted["rage"] = False
        return WaitAction(self.entity).perform()


# This AI is for enemy that attacks with a basic ranged attack
class HostileRangedEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:        
        # If the entity is confused, it does a BumpAction with a random direction
        if self.entity.status.dict_condition_afflicted["confusion"]:
            return BumpAction(self.entity, 1, 1).perform()
        # If the entity is charmed, it attacks the closest actor (not the player) or it moves close to it, otherwise it waits
        # If the entity is enraged, it attacks the closest actor or it moves close to it, otherwise it waits 
        # If it's not both, it attacks the player or it moves close to it, otherwise it waits
        else:
            if not ((self.entity.status.check_turns_charm and self.entity.status.dict_condition_afflicted["charm"]) or (self.entity.status.check_turns_rage and self.entity.status.dict_condition_afflicted["rage"])) or (not self.entity.status.dict_condition_afflicted["charm"] and self.entity.status.dict_condition_afflicted["rage"]):
                
                #The target is chosen depending on the status
                if self.entity.status.dict_condition_afflicted["charm"]:
                    self.entity.status.dict_turns_passed["charm"] += 1
                    target = self.engine.game_map.get_closest_actor(self.entity, 15, False)
                elif self.entity.status.dict_condition_afflicted["rage"]:
                    self.entity.status.dict_turns_passed["rage"] += 1
                    target = self.engine.game_map.get_closest_actor(self.entity, 15, True)
                else:
                    target = self.engine.player
                    
                if target:
                    dx = target.x - self.entity.x
                    dy = target.y - self.entity.y
                    distance = max(abs(dx), abs(dy)) # Chebyshev distance.
                    if self.engine.game_map.visible[self.entity.x, self.entity.y]:
                        if distance <= 3 and ((dx != 0 and self.entity.y == target.y) or (dy != 0 and self.entity.x == target.x)) and self.entity.status.dict_condition_afflicted["stun"] == False:
                            return RangedAction(self.entity, dx, dy).perform()
                        
                        self.path = self.get_path_to(target.x, target.y)

                         # If the entity is not afraid, it moves in the direction of the player
                        if not self.entity.status.dict_condition_afflicted["fear"]:
                            # If the entity is not blind, it moves in the direction of the player
                            if not self.entity.status.dict_condition_afflicted["blindness"]:
                                if self.path:
                                    dest_x, dest_y = self.path.pop(0)
                                    return BumpAction(
                                        self.entity,
                                        dest_x - self.entity.x,
                                        dest_y - self.entity.y,
                                    ).perform()
                            #If the entity is blind, it moves in a random direction as the confusion status
                            else:
                                return BumpAction(self.entity, dx, dy).perform()
                            
                        # If the entity is afraid, it moves in the direction contrary of the player
                        else:
                            if self.path:
                                dest_x, dest_y = self.path.pop(0)
                                return BumpAction(
                                    self.entity,
                                    -(dest_x - self.entity.x),
                                    -(dest_y - self.entity.y),
                                ).perform()
            else:
                if self.entity.status.dict_condition_afflicted["charm"]:
                    self.engine.message_log.add_message(f"The {self.entity.name} is no longer charmed.")
                    self.entity.status.dict_turns_passed["charm"] = 0
                    self.entity.status.dict_condition_afflicted["charm"] = False
                elif self.entity.status.dict_condition_afflicted["rage"]:
                    self.engine.message_log.add_message(f"The {self.entity.name} is no longer enraged.")
                    self.entity.status.dict_turns_passed["rage"] = 0
                    self.entity.status.dict_condition_afflicted["rage"] = False
        return WaitAction(self.entity).perform()


# This AI is for enemy that uses special attacks
class SpecialEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:
        target = self.engine.player

        dx = target.x - self.entity.x
        dy = target.y - self.entity.y
        distance = max(abs(dx), abs(dy))
        if self.engine.game_map.visible[self.entity.x, self.entity.y]:
            if distance <= 1:
                if self.entity.special_attacks.check_for_special_attack_ready:
                    if self.entity.special_attacks.dict_turns_recharge["percentile"] >= self.entity.special_attacks.turns_to_recharge:
                        self.entity.special_attacks.dict_turns_recharge["percentile"] = 0
                    elif self.entity.special_attacks.dict_turns_recharge["stats_drain"] >= self.entity.special_attacks.turns_to_recharge:
                        self.entity.special_attacks.dict_turns_recharge["stats_drain"] = 0
                    elif self.entity.special_attacks.dict_turns_recharge["rot"] >= self.entity.special_attacks.turns_to_recharge:
                        self.entity.special_attacks.dict_turns_recharge["rot"] = 0
                    elif self.entity.special_attacks.dict_turns_recharge["corrosion"] >= self.entity.special_attacks.turns_to_recharge:
                        self.entity.special_attacks.dict_turns_recharge["corrosion"] = 0
                    elif self.entity.special_attacks.dict_turns_recharge["ingest"] >= self.entity.special_attacks.turns_to_recharge:
                        self.entity.special_attacks.dict_turns_recharge["ingest"] = 0
                    elif self.entity.special_attacks.dict_turns_recharge["dispel"] >= self.entity.special_attacks.turns_to_recharge:
                        self.entity.special_attacks.dict_turns_recharge["dispel"] = 0
                    elif self.entity.special_attacks.dict_turns_recharge["steal"] >= self.entity.special_attacks.turns_to_recharge:
                        self.entity.special_attacks.dict_turns_recharge["steal"] = 0
                    return SpecialAttackAction(self.entity, dx, dy).perform()
                else:
                    if self.entity.special_attacks.check_attack_percentile:
                        self.entity.special_attacks.dict_turns_recharge["percentile"] += 1
                    elif self.entity.special_attacks.check_attack_stats:
                        self.entity.special_attacks.dict_turns_recharge["stats_drain"] += 1
                    elif self.entity.special_attacks.check_attack_rot:
                        self.entity.special_attacks.dict_turns_recharge["rot"] += 1
                    elif self.entity.special_attacks.check_attack_corrosion:
                        self.entity.special_attacks.dict_turns_recharge["corrosion"] += 1
                    elif self.entity.special_attacks.check_attack_ingest:
                        self.entity.special_attacks.dict_turns_recharge["ingest"] += 1
                    elif self.entity.special_attacks.check_attack_dispel:
                        self.entity.special_attacks.dict_turns_recharge["dispel"] += 1
                    elif self.entity.special_attacks.check_attack_steal:
                        self.entity.special_attacks.dict_turns_recharge["steal"] += 1
                    return MeleeAction(self.entity, dx, dy).perform()
                

            self.path = self.get_path_to(target.x, target.y)
            
            if self.path:
                dest_x, dest_y = self.path.pop(0)
                return MovementAction(self.entity, dest_x - self.entity.x, dest_y - self.entity.y).perform()
            
        return WaitAction(self).perform()