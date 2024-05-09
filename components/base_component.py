from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_logic.engine import Engine
    from entity.entity import Entity
    from game_map.game_map import GameMap


class BaseComponent:
    parent: Entity  # Owning entity instance.

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    @property
    def engine(self) -> Engine:
        return self.gamemap.engine
