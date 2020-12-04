from typing import Optional

from game_map.interactive_object import InteractiveObject
from game_map.area.tiles.tile_layers.abstract_tile_layer import TileLayer
from game_map.area.area import Area, Point


class BasicTile(Area):

    def __init__(self, y: int, x: int, height: float = 0):
        bottom_left = Point(y, x)
        top_right = Point(y + 1, x + 1)
        super().__init__(bottom_left, top_right)
        self._height = height

    @property
    def height(self):

        return self._height

    @staticmethod
    def is_tile_layer(inter_object: InteractiveObject) -> bool:

        result = isinstance(inter_object, TileLayer)

        return result

    def add_object(self, inter_object: InteractiveObject):

        if BasicTile.is_tile_layer(inter_object):
            tiles_in_container = map(BasicTile.is_tile_layer, self.container)

            if any(tiles_in_container):
                error_message = 'Only one internal TileLayer is allowed'
                raise InteractiveObject.AddingObjectError(error_message)

        super().add_object(inter_object)

    @property
    def top_layer(self) -> Optional[TileLayer]:

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
