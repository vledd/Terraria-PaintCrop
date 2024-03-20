from enum import Enum

TILE_SIZE_PX: int = 16
TILE_SIZE_OFFSET_PX: int = 18  # Tile size with two blank pixels after it


class TilesetTilesOrder(Enum):
    LEFT2RIGHT = 0,
    UP2DOWN = 1
