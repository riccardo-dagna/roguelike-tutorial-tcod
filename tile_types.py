from typing import Tuple
import numpy as np  # type: ignore

np.bool = np.bool_

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype( #create a datatype similar to a struct in C
    [
        ("ch", np.int32),  # Unicode codepoint. Represent the character
        ("fg", "3B"),  # 3 unsigned bytes, for RGB colors. Represent the foreground color
        ("bg", "3B"),  # 3 unsigned bytes, for RGB colors. Represent the background color
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool),  # True if this tile can be walked over.
        ("transparent", np.bool),  # True if this tile doesn't block FOV.
        ("dark", graphic_dt),  # Graphics for when this tile is not in FOV.
        ("light", graphic_dt)  # Graphics for when this tile is in FOV.
    ]
)

#SHROUD represent unexplored unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)


floor = new_tile(
    walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255), (50, 50, 150)), light=(ord(" "), (255, 255, 255), (200, 180, 50))
)
wall = new_tile(
    walkable=False, transparent=False, dark=(ord(" "), (255, 255, 255), (0, 0, 100)), light=(ord(" "), (255, 255, 255), (130, 110, 50))
)