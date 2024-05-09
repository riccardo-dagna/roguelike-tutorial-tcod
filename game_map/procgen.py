from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Iterator, List, Tuple
import random
import copy

import tcod

from game_map.game_map import GameMap
import entity.entity_factories as entity_factories
import game_map.tile_types as tile_types

if TYPE_CHECKING:
    from game_logic.engine import Engine
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
    0: [(entity_factories.stun_scroll, 80)],
    0: [(entity_factories.confusion_scroll, 80)],
    2: [(entity_factories.health_potion, 35)],
    2: [(entity_factories.status_potion, 35)],
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


def get_max_value_for_floor(max_value_by_floor: List[Tuple[int, int]], floor: int) -> int:
    current_value = 0

    for floor_minimum, value in max_value_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_value = value

    return current_value


def get_entities_at_random(
    weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
    number_of_entities: int,
    floor: int,
) -> List[Entity]:
    entity_weighted_chances = {}

    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                entity = value[0]
                weighted_chance = value[1]

                entity_weighted_chances[entity] = weighted_chance

    entities = list(entity_weighted_chances.keys())
    entity_weighted_chance_values = list(entity_weighted_chances.values())

    chosen_entities = random.choices(entities, weights=entity_weighted_chance_values, k=number_of_entities)

    return chosen_entities

def get_chest_item_at_random(
    weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
    floor: int
) -> Item:
    item_weighted_chances = {}
    
    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                item = value[0]
                weighted_chance = value[1]

                item_weighted_chances[item] = weighted_chance
    
    items_list = list(item_weighted_chances.keys())
    item_weighted_chances_values = list(item_weighted_chances.values())
    
    chosen_item = random.choices(items_list, weights=item_weighted_chances_values, k=1)
    return chosen_item[0]


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return self.x1 <= other.x2 and self.x2 >= other.x1 and self.y1 <= other.y2 and self.y2 >= other.y1


def place_entities(room: RectangularRoom, dungeon: GameMap, floor_number: int) -> None:
    number_of_monsters = random.randint(0, get_max_value_for_floor(max_monsters_by_floor, floor_number))
    number_of_items = random.randint(0, get_max_value_for_floor(max_items_by_floor, floor_number))

    monsters: List[Entity] = get_entities_at_random(enemy_chances, number_of_monsters, floor_number)
    items: List[Entity] = get_entities_at_random(item_chances, number_of_items, floor_number)

    for entity in monsters + items:
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn(dungeon, x, y)


def tunnel_between(start: Tuple[int, int], end: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y


def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    engine: Engine,
) -> GameMap:
    """Generate a new dungeon map."""
    player = engine.player
    dungeon = GameMap(engine, map_width, map_height, entities=[player])

    rooms: List[RectangularRoom] = []

    center_of_last_room = (0, 0)

    total_chest = 0

    for _ in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Dig out this rooms inner area.
        dungeon.tiles[new_room.inner] = tile_types.floor
        
        #Create a chest in the room, if the total of chest is minor to the max number of chest
        if total_chest <= max_chest_by_floor:
            x = random.randint(new_room.x1 + 1, new_room.x2 - 1)
            y = random.randint(new_room.y1 + 1, new_room.y2 - 1)

            if not any (chest.x == x and chest.y == y for chest in dungeon.chests):
                if random.random() < 0.7:
                    pass
                else:
                    dungeon.tiles[x, y] = tile_types.chest
                    entity_factories.chest.spawn(gamemap=dungeon, x=x, y=y, item=get_chest_item_at_random(chest_chances, floor=engine.game_world.current_floor))
                    total_chest += 1


        if len(rooms) == 0:
            # The first room, where the player starts.
            player.place(*new_room.center, dungeon)
        else:  # All rooms after the first.
            # Dig out a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

            center_of_last_room = new_room.center

        place_entities(new_room, dungeon, engine.game_world.current_floor)

        dungeon.tiles[center_of_last_room] = tile_types.down_stairs
        dungeon.downstairs_location = center_of_last_room

        # Finally, append the new room to the list.
        rooms.append(new_room)

    return dungeon
