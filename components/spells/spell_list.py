from __future__ import annotations

from typing import TYPE_CHECKING, Any

from actions_logic.input_handlers import SelectIndexHandler, SingleRangedAttackHandler, AreaRangedAttackHandler
from components.base_component import BaseComponent
from components.spells.spell import Spell
from entity.entity import Entity
from game_logic.engine import Engine

class Fireball(Spell):
    def __init__(self, parent: Entity) -> None:
        super().__init__(name="Fireball", damage=12, mana=1, radius=3, type="damage", parent=parent, handler=AreaRangedAttackHandler)

class LightningBolt(Spell):
    def __init__(self, parent: Entity) -> None:
        super().__init__(name="Lightning bolt", damage=20, mana=1, max_range=5, type="damage", parent=parent,)

class IceDart(Spell):
    def __init__(self, parent: Entity) -> None:
        super().__init__(name="Ice dart", damage=20, mana=1, type="damage", parent=parent, handler=SingleRangedAttackHandler)

class Confusion(Spell):
    def __init__(self, parent: Entity) -> None:
        super().__init__(name="Confusion", mana=1, status="confusion", type="status", parent=parent, handler=SingleRangedAttackHandler)

class Fear(Spell):
    def __init__(self, parent: Entity) -> None:
        super().__init__(name="Fear", mana=1, status="fear", type="status", parent=parent, handler=SingleRangedAttackHandler)

class Stun(Spell):
    def __init__(self, parent: Entity) -> None:
        super().__init__(name="Stun", mana=1, status="stun", type="status", parent=parent, handler=SingleRangedAttackHandler)

class Heal(Spell):
    def __init__(self, parent: Entity) -> None:
        super().__init__(name="Heal", damage=10, mana=1, type="cure", parent=parent)

