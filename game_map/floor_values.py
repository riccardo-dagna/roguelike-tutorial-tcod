from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Tuple
import entity.entity_factories as entity_factories

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
    0: [(entity_factories.health_potion, 35)],
    0: [(entity_factories.status_potion, 35)],
    2: [(entity_factories.stun_scroll, 80)],
    2: [(entity_factories.confusion_scroll, 80)],
    4: [(entity_factories.lightning_scroll, 25)],
    6: [(entity_factories.fireball_scroll, 25)],
}

# This is the dictionary that contain the spawning enemy and weight
enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.orc, 80)],
    3: [(entity_factories.troll, 15)],
    5: [(entity_factories.troll, 30)],
    7: [(entity_factories.troll, 60)],
}

# This is the dictionary that contain the spawning items in chances and weight
chest_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.sword, 80), (entity_factories.chain_mail, 80)],
    2: [(entity_factories.sword, 0), (entity_factories.chain_mail, 0), (entity_factories.attack_ring, 80), (entity_factories.defense_ring, 80)],
    4: [(entity_factories.sword, 0), (entity_factories.chain_mail, 0), (entity_factories.attack_ring, 15), (entity_factories.defense_ring, 15), (entity_factories.vorpal_sword, 60)],
}
