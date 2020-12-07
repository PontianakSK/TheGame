from typing import Optional

from game_map.area.tiles.tiles import BasicTile  # type: ignore
from game_map.area.area import Area, Point  # type: ignore


class GameMap(Area):

    '''
    Area object that containes all map tiles
    in one game. Is Singleton.
    '''

    # used for singleton realization
    _instance: Optional['GameMap'] = None
    _initialized: bool = False

    @staticmethod
    def __new__(cls, bottom_left: Point, top_right: Point) -> 'GameMap':

        if not cls._instance:
            cls._instance = super(GameMap, cls).__new__(cls)

        return cls._instance

    def __init__(self, bottom_left: Point, top_right: Point) -> None:

        if (GameMap._initialized):
            return
        super().__init__(bottom_left, top_right)
        GameMap._initialized = True

    def tile(self, y: int, x: int) -> BasicTile:
        '''
        Used to get tiles by coordinates (tiles
        are stored in flat list).
        '''

        result = super().get_object(y, x)

        return result

    def __repr__(self, *args, **kwargs):

        info = [
            f'size_y: {self.size_y}',
            f'size_x: {self.size_x}',
        ]

        return super().__repr__(*args, **kwargs, info=info)

    def add_object(self, inter_object: BasicTile) -> None:
        '''
        GameMap should contain only tile objects. All other
        objects should be placed inside tiles.
        '''

        if isinstance(inter_object, BasicTile):
            super().add_object(inter_object)
            return

        exception_message = 'Map should contains BasicTiles only!'

        raise BasicTile.AddingObjectError(exception_message)
