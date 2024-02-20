from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor

class Status(BaseComponent):
    parent: Actor

    damage_burn: int = 1
    damage_poison: int = 2
    turns_poison: int = 4
    turns_burn: int = 4

    def __init__(self, 
                 flag_burn: bool = False, 
                 flag_poison: bool = False,
                 immunity_burn: bool = False,
                 immunity_poison: bool = False
    ):
        self.flag_burn = flag_burn
        self.flag_poison = flag_poison
        self.immunity_burn = immunity_burn
        self.immunity_poison = immunity_poison
        self.turns_passed = 0
    
    @property
    def check_turns_poison(self) -> bool:
        return self.flag_poison and self.turns_passed > self.turns_poison
        
    @property
    def check_turns_burns(self) -> bool:
        return self.flag_burn and self.turns_passed > self.turns_burn
    
    @property
    def check_burn_immunity(self) -> bool:
        return self.immunity_burn
    
    @property
    def check_poison_immunity(self) -> bool:
        return self.immunity_poison
        
    def effect_hp_damage(self) -> None:
        if self.flag_burn:
            self.parent.fighter.hp -= self.damage_burn
            self.engine.message_log.add_message(f"You receive {self.damage_burn} damage from the burn!")
            self.turns_passed = 0
        if self.flag_poison:
            self.parent.fighter.hp -= self.damage_poison
            self.engine.message_log.add_message(f"You receive {self.damage_poison} damage from the poison!")
            self.turns_passed = 0

    