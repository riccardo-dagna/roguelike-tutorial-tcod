from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple, Type, TypeVar, Union
import copy
import math

from render_logic.render_order import RenderOrder

if TYPE_CHECKING:
    from components.ai import BaseAI
    from components.item.consumable import Consumable
    from components.damageinfo import DamageInfo
    from components.item.equipment import Equipment
    from components.item.equippable import Equippable
    from components.classes.character_class import CharacterClass
    from components.classes.fighter import Fighter
    from components.inventory import Inventory
    from components.level import Level
    from components.special_attacks import SpecialAttacks
    from components.status import Status
    from game_map import GameMap
    from components.spells.spellbook import Spellbook
    from components.spells.spell import Spell

T = TypeVar("T", bound="Entity")


class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    parent: Union[GameMap, Inventory]

    def __init__(
        self,
        parent: Optional[GameMap] = None,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order
        if parent:
            # If parent isn't provided now then it will be set later.
            self.parent = parent
            parent.entities.add(self)

    @property
    def gamemap(self) -> GameMap:
        return self.parent.gamemap

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.parent = gamemap
        gamemap.entities.add(clone)
        return clone

    def place(self, x: int, y: int, gamemap: Optional[GameMap] = None) -> None:
        """Place this entitiy at a new location.  Handles moving across GameMaps."""
        self.x = x
        self.y = y
        if gamemap:
            if hasattr(self, "parent"):  # Possibly uninitialized.
                if self.parent is self.gamemap:
                    self.gamemap.entities.remove(self)
            self.parent = gamemap
            gamemap.entities.add(self)

    def distance(self, x: int, y: int) -> float:
        """
        Return the distance between the current entity and the given (x, y) coordinate.
        """
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move(self, dx: int, dy: int) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy


class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        ai_cls: Type[BaseAI],
        equipment: Equipment,
        fighter: CharacterClass,
        inventory: Inventory,
        level: Level,
        status: Status,
        damage_info: DamageInfo,
        special_attacks: SpecialAttacks,
        spellbook: Spellbook,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
            render_order=RenderOrder.ACTOR,
        )

        self.ai: Optional[BaseAI] = ai_cls(self)

        self.equipment: Equipment = equipment
        self.equipment.parent = self

        self.fighter = fighter
        self.fighter.parent = self

        self.inventory = inventory
        self.inventory.parent = self

        self.level = level
        self.level.parent = self

        self.status = status
        self.status.parent = self

        self.damage_info = damage_info
        self.damage_info.parent = self
        
        self.special_attacks = special_attacks
        self.special_attacks.parent = self

        self.spellbook = spellbook
        self.spellbook.parent = self


    @property
    def is_alive(self) -> bool:
        """Returns True as long as this actor can perform actions."""
        return bool(self.ai)


class Item(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        material: str = "",
        scroll: bool = False,
        spell_correspondent: Spell = None,
        magic_item: bool = False,
        damaged: bool = False,
        consumable: Optional[Consumable] = None,
        equippable: Optional[Equippable] = None,
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=False,
            render_order=RenderOrder.ITEM,
        )

        self.material = material
        self.magic_item = magic_item
        self.damaged = damaged
        self.scroll = scroll

        self.consumable = consumable

        if self.consumable:
            self.consumable.parent = self

        self.equippable = equippable
        
        self.spell_correspondent = spell_correspondent

        if self.equippable:
            self.equippable.parent = self
    
    @property
    def is_organic(self) -> bool:
        return self.material == "paper" or self.material == "leather" or self.material == "wood"
    
    @property
    def is_metallic(self) -> bool:
        return self.material == "metal" 


class Chest(Entity):
    def __init__(
            self,
            *,
            x: int = 0,
            y: int = 0,
            char: str = "?",
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            item: Item = None,
            locked: bool = False
    ):
        super().__init__(x=x, y=y, char=char, color=color, name=name, blocks_movement=True, render_order=RenderOrder.ACTOR)

        self.item = item
        self.opened = False
        self.locked = locked

    def spawn(self: T, gamemap: GameMap, x: int, y: int, item: Item) -> T:
        """Spawn a copy of this chest at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.item = item
        clone.parent = gamemap
        gamemap.chests.add(clone)
        return clone


