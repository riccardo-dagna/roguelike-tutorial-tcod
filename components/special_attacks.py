from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional
import random

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity.entity import Actor

class SpecialAttacks(BaseComponent):
    parent: Actor

    def __init__(self) -> None:
        pass


