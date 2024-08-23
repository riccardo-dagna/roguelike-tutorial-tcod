from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Optional, List
import random

from components.base_component import BaseComponent
from utility_files.exceptions import Impossible

if TYPE_CHECKING:
    from entity.entity import Actor
    from game_logic.engine import Engine
    from components.spells.spell import Spell

class Spellbook(BaseComponent):
    parent: Actor

    def __init__(self, capacity: int = 0, start_list: List[Spell] = [],) -> None:
        self.capacity = capacity
        self.spells = start_list

    def check_if_spell_is_present(self, spell_to_add: Spell) -> bool:
        """
        Add a spell to the spellbook. If it's already present, it does nothing
        """
        spell_present = False
        for spell in self.spells:
                if spell_to_add.name == spell.name and not spell_present:
                    spell_present = True
        return spell_present

