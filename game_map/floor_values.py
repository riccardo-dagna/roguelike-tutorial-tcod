from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Tuple
from entity.entity_factories import equipment
from entity.entity_factories import consumable
from entity.entity_factories import enemies

if TYPE_CHECKING:
    from entity.entity import Entity, Item

# This is the list of the max enemy, item in floor and item in chests per floor
"""max_chest_by_floor = [
    (1, 1),
    (4, 2),
]"""

max_chest_by_floor = 2

max_items_by_floor = [
    (1, 1),
    (4, 2),
]

max_monsters_by_floor = [
    (1, 2),
    (4, 3),
    (6, 5),
]

# This is the dictionary that contain the spawning items on the floor and weight
item_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(consumable.health_potion, 35), (consumable.status_potion, 35), (consumable.mana_potion, 35)],
    2: [(consumable.stun_scroll, 80)],
    2: [(consumable.confusion_scroll, 80)],
    4: [(consumable.lightning_scroll, 25)],
    6: [(consumable.fireball_scroll, 25)],
}

# This is the dictionary that contain the spawning enemy and weight
enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(enemies.meelee_orc, 80), (enemies.ranged_orc, 80)],
    #0: [(enemies.vampire, 80)],
    #0: [(enemies.magic_orc, 80)],
    3: [(enemies.troll, 15)],
    5: [(enemies.troll, 30)],
    7: [(enemies.troll, 60)],
}

# This is the dictionary that contain the spawning items in chances and weight
chest_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(equipment.sword, 80), (equipment.chain_mail, 80)],
    2: [(equipment.sword, 0), (equipment.chain_mail, 0), (equipment.attack_ring, 80), (equipment.defense_ring, 80)],
    4: [(equipment.sword, 0), (equipment.chain_mail, 0), (equipment.attack_ring, 15), (equipment.defense_ring, 15), (equipment.vorpal_sword, 60)],
}
