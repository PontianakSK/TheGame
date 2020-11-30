from typing import Optional

from game_map.interactive_object import InteractiveObject
from game_map.tiles.tile_layers.abstract_tile_layer import TileLayer


class BasicTile(InteractiveObject):

    def __init__(self, height: float = 0):
        super().__init__()
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
