from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_components import BaseComponent

if TYPE_CHECKING:
    from entity import Actor

class Fighter(BaseComponent):
    entity: Actor

    def __init__(self, hp: int, power: int, defense: int):
        self.max_hp = hp
        self._hp = hp
        self.power = power
        self.defense = defense

    @property
    def hp(self) -> int:
        return self._hp
    
    @property
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.max_hp))
        if self._hp == 0 and self.entity.ai:
            self.die()

    def die(self) -> None:
        if self.engine.player is self.entity:
            death_message = "You died!"
        else:
            death_message = f"{self.entity.name} is dead!"
        
        self.entity.char = "%"
        self.entity.color = (191, 0, 0)
        self.entity.blocks_movement = False
        self.entity.ai = None
        self.entity.name = f"remains of {self.entity.name}"

        print (death_message)
