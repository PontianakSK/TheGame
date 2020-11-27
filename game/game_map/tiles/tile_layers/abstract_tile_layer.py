from typing import Optional, Literal

from game_map.interactive_object import InteractiveObject

class TileLayer(InteractiveObject):

    def __init__(self, lower_layer: Optional['TileLayer']=None):

        super().__init__()
        self.add_object(lower_layer)
        self._fertility = 1


    def add_object(self, inter_object: InteractiveObject):

        if isinstance(inter_object, TileLayer):
            for owned_object in self.container:
                if isinstance(owned_object, TileLayer):
                    raise InteractiveObject.AddingObjectError('Only one internal TileLayer is allowed')
        super().add_object(inter_object)


    def accept_damage(self, damage):

        for owned_object in self.container:
            if not isinstance(owned_object, TileLayer):
                owned_object.accept_damage(damage)


    @property
    def lower_layer(self)->Optional['TileLayer']:

        for inter_object in self.container:
            if isinstance(inter_object, TileLayer):
                return inter_object
        return None


    @lower_layer.setter
    def lower_layer(self, tile_layer: Optional['TileLayer'])->None:
        
        self.add_object(tile_layer)


    @property
    def fertility(self)->float:

        return self._fertility
        
    def __repr__(self):
        info = [
            f'fertility: {self.fertility}'
        ]
        return super().__repr__(info=info)
    

        


if __name__ == '__main__':
   top_layer = TileLayer()
   top_layer.upper_layer = TileLayer()
   top_layer.upper_layer._is_passable = False
   top_layer.container.append('fish')
   print(top_layer)

