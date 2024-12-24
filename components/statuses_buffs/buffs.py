from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional
import random

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity.entity import Actor
    from game_logic.engine import Engine

class Buffs(BaseComponent):
    parent: Actor

    turns_haste = 10

    def __init__(self,
                 flag_haste: bool = False, flag_strenght: bool = False, flag_defense: bool = False, flag_dexterity: bool = False, flag_revive: bool = False,
    ):
        self.dict_flag_buffs = dict(haste = flag_haste, strenght = flag_strenght, defense = flag_defense, dexterity = flag_dexterity, revive=flag_revive,)
        self.dict_turns_passed = dict(haste = 0,)

