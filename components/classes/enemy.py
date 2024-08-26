from __future__ import annotations

from typing import TYPE_CHECKING

#from components.base_component import BaseComponent
from render_logic.render_order import RenderOrder
import game_map.color as color
from components.classes.character_class import CharacterClass

if TYPE_CHECKING:
    from entity.entity import Actor

class EnemyClass(CharacterClass):
    parent: Actor

    def __init__(self, hp: int, base_defense: int, base_power: int, mana: int = 0):
        super().__init__(hp, base_defense, base_power, mana)