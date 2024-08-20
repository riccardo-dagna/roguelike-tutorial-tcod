from __future__ import annotations

from typing import TYPE_CHECKING, Any

from actions_logic.input_handlers import SelectIndexHandler
from components.base_component import BaseComponent
from components.spells.spell import Spell
from actions_logic.input_handlers import SingleRangedAttackHandler, AreaRangedAttackHandler
from entity.entity import Entity
from game_logic.engine import Engine

class Fireball(Spell):
    def __init__(self, parent: Entity) -> None:
        super().__init__(name="Fireball", damage=12, mana=1, max_range=0, radius=3, status=None, type="damage", parent=parent, handler=AreaRangedAttackHandler)

class LightningBolt(Spell):
    def __init__(self, parent: Entity) -> None:
        super().__init__(name="Lightning bolt", damage=20, mana=1, max_range=5, radius=0, status=None, type="damage", parent=parent, handler=None)

class IceDart(Spell):
    def __init__(self, parent: Entity) -> None:
        super().__init__(name="Ice dart", damage=20, mana=1, max_range=0, radius=0, status=None, type="damage", parent=parent, handler=SingleRangedAttackHandler)




