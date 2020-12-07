from typing import Optional

from game_map.interactive_object import InteractiveObject
from game_map.area.tiles.tile_layers.abstract_tile_layer import TileLayer
from game_map.area.area import Area, Point


class BasicTile(Area):
    '''
    Simple tile object. Represent smallest part
    of the Game map.
    '''

    def __init__(self, y: int, x: int, height: float = 0):
        bottom_left = Point(y, x)
        top_right = Point(y + 1, x + 1)
        super().__init__(bottom_left, top_right)
        self._height = height

    @property
    def height(self):
        '''
        Height of tile affects type of landscape in some
        builders. Also affects weather.
        '''

        return self._height

    @staticmethod
    def is_tile_layer(inter_object: InteractiveObject) -> bool:
        '''
        Just checks if object is TileLayer
        '''

        result = isinstance(inter_object, TileLayer)

        return result

    def add_object(self, inter_object: InteractiveObject):
        '''
        Tiles can contain any object. But only one TileLayer.
        lower layers should contain each other.
        '''

        if BasicTile.is_tile_layer(inter_object):
            tiles_in_container = map(BasicTile.is_tile_layer, self.container)

            if any(tiles_in_container):
                error_message = 'Only one internal TileLayer is allowed'
                raise InteractiveObject.AddingObjectError(error_message)

        super().add_object(inter_object)

    @property
    def top_layer(self) -> Optional[TileLayer]:
        '''
        Returns top layer of this tile if it exists.
        Returns None otherwise.
        '''

        for obj in self.container:

            if isinstance(obj, TileLayer):

                return obj

        return None

    def __repr__(self, *args, **kwargs):

        info = [
            f'height: {self._height}',
            f'coordinates: {self.bottom_left}',
            ]
        result = super().__repr__(*args, **kwargs, info=info)

        return result
