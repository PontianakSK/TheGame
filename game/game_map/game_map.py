from typing import Optional

from game_map.tiles.tiles import BasicTile  # type: ignore
from game_map.interactive_object import InteractiveObject  # type: ignore


class Area(InteractiveObject):

    pass


class GameMap(Area):

    _instance: Optional['GameMap'] = None
    _initialized: bool = False

    @staticmethod
    def __new__(cls, size_y, size_x):

        if not cls._instance:
            cls._instance = super(GameMap, cls).__new__(cls)

        return cls._instance

    def __init__(self, size_y: int, size_x: int) -> None:

        if (GameMap._initialized):
            return
        super().__init__()
        self.size_y = size_y
        self.size_x = size_x
        GameMap._initialized = True

    def tile(self, y: int, x: int) -> BasicTile:

        raise NotImplementedError

    def __repr__(self, *args, **kwargs):

        info = [
            f'size_y: {self.size_y}',
            f'size_x: {self.size_x}',
        ]

        return super().__repr__(*args, **kwargs, info=info)

    def add_object(self, inter_object: InteractiveObject) -> None:

        if isinstance(inter_object, BasicTile):
            super().add_object(inter_object)
            return

        exception_message = 'Map should contains BasicTiles only!'

        raise InteractiveObject.AddingObjectError(exception_message)
