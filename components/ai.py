from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Tuple
import random

import numpy as np
import tcod

from actions_logic.actions import Action, BumpAction, MeleeAction, MovementAction, WaitAction
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


class HostileEnemy(BaseAI):
    def __init__(self, entity: Actor):
        super().__init__(entity)
        self.path: List[Tuple[int, int]] = []

    def perform(self) -> None:        
        # If the entity is confused, it does a BumpAction with a random direction
        if self.entity.status.dict_condition_afflicted["confusion"]:
            return BumpAction(self.entity, 1, 1).perform()
        # If the entity is charmed, it attacks the closest enemy of the player, otherwise it waits
        elif self.entity.status.dict_condition_afflicted["charm"]:
            if not self.entity.status.check_turns_charm:
                self.entity.status.dict_turns_passed["charm"] += 1
                target = self.engine.game_map.get_closest_actor(self.entity, 8)
                if target:
                    dx = target.x - self.entity.x
                    dy = target.y - self.entity.y
                    distance = max(abs(dx), abs(dy)) # Chebyshev distance.
                    if distance <= 1:
                        return MeleeAction(self.entity, dx, dy)
                    
                    self.path = self.get_path_to(target.x, target.y)

                    if self.path:
                        dest_x, dest_y = self.path.pop(0)
                        return MovementAction(
                            self.entity,
                            dest_x - self.entity.x,
                            dest_y - self.entity.y,
                        ).perform()
                else:
                    return WaitAction(self.entity).perform()
            else:
                self.engine.message_log.add_message(f"The {self.entity.name} is no longer charmed.")
                self.entity.status.dict_turns_passed["charm"] = 0
                self.entity.status.dict_condition_afflicted["charm"] = False
                return WaitAction(self.entity).perform()

        # If the entity is not confused/charmed, it performs its normal action
        else:
            target = self.engine.player
            dx = target.x - self.entity.x
            dy = target.y - self.entity.y
            distance = max(abs(dx), abs(dy))  # Chebyshev distance.
            if self.engine.game_map.visible[self.entity.x, self.entity.y]:
                if distance <= 1:
                    return MeleeAction(self.entity, dx, dy).perform()

                self.path = self.get_path_to(target.x, target.y)
            
            # If the entity is not afraid, it moves in the direction of the player
            if not self.entity.status.dict_condition_afflicted["fear"]:
                # If the entity is not blind, it moves in the direction of the player
                if not self.entity.status.dict_condition_afflicted["blindness"]:
                    if self.path:
                        dest_x, dest_y = self.path.pop(0)
                        return MovementAction(
                            self.entity,
                            dest_x - self.entity.x,
                            dest_y - self.entity.y,
                        ).perform()
                else:
                    return BumpAction(self.entity, dx, dy).perform()

            # If the entity is afraid, it moves in the direction contrary of the player
            else:
                if self.path:
                    dest_x, dest_y = self.path.pop(0)
                    return MovementAction(
                        self.entity,
                        -(dest_x - self.entity.x),
                        -(dest_y - self.entity.y),
                    ).perform()

        return WaitAction(self.entity).perform()
