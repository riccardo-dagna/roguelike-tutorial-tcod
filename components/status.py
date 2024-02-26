from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional
import random

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor

class Status(BaseComponent):
    parent: Actor

    damage_bleed: int = 1
    damage_poison: int = 2
    turns_poison: int = 4
    turns_bleed: int = 4
    turns_stun: int = 1
    turns_confusion: int = 5

    def __init__(self, 
                 flag_bleed: bool = False, flag_poison: bool = False, flag_stun: bool = False, flag_confusion: bool = False, flag_grab: bool = False,
                 immunity_bleed: bool = False, immunity_poison: bool = False, immunity_stun: bool = False, immunity_confusion: bool = False, immunity_grab: bool = False,
                 attack_bleed: bool = False, attack_poison: bool = False, attack_stun: bool = False, attack_confusion: bool = False, attack_grab: bool = False,
    ):
        self.dict_condition_afflicted = dict(flag_bleed = flag_bleed, flag_poison = flag_poison, flag_stun = flag_stun, flag_confusion = flag_confusion, 
                                             flag_grab = flag_grab
                                             )

        self.dict_condition_immunity = dict(immunity_bleed = immunity_bleed, immunity_poison = immunity_poison, immunity_stun = immunity_stun, immunity_confusion = immunity_confusion, 
                                            immunity_grab = immunity_grab
                                            )

        self.dict_condition_attack = dict(attack_bleed = attack_bleed, attack_poison = attack_poison, attack_stun = attack_stun, attack_confusion = attack_confusion, 
                                          attack_grab = attack_grab
                                          )

        self.turns_passed = 0
    
    @property
    def check_turns_poison(self) -> bool:
        return self.dict_condition_afflicted["flag_bleed"] and self.turns_passed > self.turns_poison
        
    @property
    def check_turns_bleed(self) -> bool:
        return self.dict_condition_afflicted["flag_poison"] and self.turns_passed > self.turns_bleed
    
    @property
    def check_turns_stun(self) -> bool:
        return self.turns_passed >= self.turns_stun
    
    @property
    def check_turns_confusion(self) -> bool:
        return self.turns_passed > self.turns_confusion
    
    @property
    def check_grabbed_condition(self) -> bool:
        return self.dict_condition_afflicted["flag_grab"]

    @property
    def check_bleed_immunity(self) -> bool:
        return self.dict_condition_immunity["immunity_bleed"]
    
    @property
    def check_poison_immunity(self) -> bool:
        return self.dict_condition_immunity["immunity_poison"]
    
    @property
    def check_stun_immunity(self) -> bool:
        return self.dict_condition_immunity["immunity_stun"]
    
    @property
    def check_confusion_immunity(self) -> bool:
        return self.dict_condition_immunity["immunity_confusion"]
    
    @property
    def check_grab_immunity(self) -> bool:
        return self.dict_condition_immunity["immunity_grab"]
        
    def effect_hp_damage(self) -> None:
        if self.dict_condition_afflicted["flag_bleed"]:
            self.parent.fighter.hp -= self.damage_bleed
            self.engine.message_log.add_message(f"You receive {self.damage_bleed} damage from the bleeding!")
            self.turns_passed = 0
        if self.dict_condition_afflicted["flag_poison"]:
            self.parent.fighter.hp -= self.damage_poison
            self.engine.message_log.add_message(f"You receive {self.damage_poison} damage from the poison!")
            self.turns_passed = 0

    def confusion_direction(self) -> Tuple[int, int]:
        # Return a random direction to the player.
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

        return direction_x, direction_y
