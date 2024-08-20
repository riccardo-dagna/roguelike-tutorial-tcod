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

    def learn_spell(self, spell_to_add: Spell) -> bool:
        """
        Add a spell to the spellbook. If it's already present, it does nothing
        """
        spell_present = False
        if len(self.spells) >= self.capacity:
            raise Impossible("Your spellbook is full.")
        else:
            for spell in self.spells:
                if spell_to_add.name == spell.name and not spell_present:
                    spell_present = True

            if spell_present:
                self.engine.message_log.add_message(f"The {spell_to_add.name} is already present in your spellbook!")
            else:
                self.spells.append(spell_to_add)
                self.engine.message_log.add_message(f"You learned the {spell_to_add.name}!")


