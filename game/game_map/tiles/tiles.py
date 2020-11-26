from game_map.tiles.tile_layers.abstract_tile_layer import TileLayer

class BasicTile:

    def __init__(self, height:float=0):
        self._height = height
        self.top_layer = TileLayer()

    @property
    def height(self):

        return self._height

    def __repr__(self):
        
        return f'{self.__class__.__name__}({id(self)}){{\n{self.height=}\n {self.top_layer}}}'
