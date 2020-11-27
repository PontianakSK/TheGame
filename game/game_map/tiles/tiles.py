from typing import Optional

from game_map.interactive_object import InteractiveObject
from game_map.tiles.tile_layers.abstract_tile_layer import TileLayer

class BasicTile(InteractiveObject):

    def __init__(self, height:float=0):
        super().__init__() 
        self._height = height

    @property
    def height(self):

        return self._height


    def add_object(self, inter_object: InteractiveObject):

        if isinstance(inter_object, TileLayer):
            for owned_object in self.container:
                if isinstance(owned_object, TileLayer):
                    raise InteractiveObject.AddingObjectError('Only one internal TileLayer is allowed')
        super().add_object(inter_object)

    @property
    def top_layer(self)->Optional[TileLayer]:

        for obj in self.container:
            if isinstance(obj, TileLayer):
                return obj
        
        return None


