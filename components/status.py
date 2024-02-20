from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor

class Status(BaseComponent):
    parent: Actor

    damage_bleed: int = 1
    damage_poison: int = 2
    turns_poison: int = 4
    turns_bleed: int = 4

    def __init__(self, 
                 flag_bleed: bool = False, 
                 flag_poison: bool = False,
                 immunity_bleed: bool = False,
                 immunity_poison: bool = False,
                 attack_bleed: bool = False,
                 attack_poison: bool = False,
    ):
        self.dict_condition_afflicted = dict(flag_bleed = flag_bleed, flag_poison = flag_poison)

        self.dict_condition_immunity = dict(immunity_bleed = immunity_bleed, immunity_poison = immunity_poison)

        self.dict_condition_attack = dict(attack_bleed = attack_bleed, attack_poison = attack_poison)

        self.turns_passed = 0
    
    @property
    def check_turns_poison(self) -> bool:
        return self.dict_condition_afflicted["flag_bleed"] and self.turns_passed > self.turns_poison
        
    @property
    def check_turns_bleed(self) -> bool:
        return self.dict_condition_afflicted["flag_poison"] and self.turns_passed > self.turns_bleed
    
    @property
    def check_bleed_immunity(self) -> bool:
        return self.dict_condition_immunity["immunity_bleed"]
    
    @property
    def check_poison_immunity(self) -> bool:
        return self.dict_condition_immunity["immunity_poison"]
        
    def effect_hp_damage(self) -> None:
        if self.dict_condition_afflicted["flag_bleed"]:
            self.parent.fighter.hp -= self.damage_bleed
            self.engine.message_log.add_message(f"You receive {self.damage_bleed} damage from the bleeding!")
            self.turns_passed = 0
        if self.dict_condition_afflicted["flag_poison"]:
            self.parent.fighter.hp -= self.damage_poison
            self.engine.message_log.add_message(f"You receive {self.damage_poison} damage from the poison!")
            self.turns_passed = 0

    