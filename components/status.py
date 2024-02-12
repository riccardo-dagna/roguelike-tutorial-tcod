from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor

class Status(BaseComponent):
    parent: Actor

    def __init__(self, damage_burn: int, damage_poison: int, 
                 turns_burn: int, turns_poison: int
    ):
        self.damage_burn = damage_burn
        self.damage_poison = damage_poison
        self.turns_burn = turns_burn
        self.turns_poison = turns_poison

    @property
    def poison_turns(self):
        return self.turns_poison

    def burn_turns(self):
        return self.turns_burn
    
        

