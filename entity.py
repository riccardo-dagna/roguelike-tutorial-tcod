from typing import Tuple

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """

    def __init__(self, x: int, y: int, char: str, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.char = char   #the character used to represent the entity
        self.color = color #the color used when drawing the entity

    def move(self, dx: int, dy: int) -> None:
        #move a entity of a given amount
        self.x += dx
        self.y += dy