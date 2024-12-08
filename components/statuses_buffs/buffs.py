from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional
import random

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity.entity import Actor
    from game_logic.engine import Engine

class Buffs(BaseComponent):
    parent: Actor

    def __init__(self,
                 flag_haste: bool = False,                 
    ):
        self.dict_flag_buffs = dict(haste = flag_haste,)