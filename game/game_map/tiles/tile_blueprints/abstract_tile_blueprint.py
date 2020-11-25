from typing import Optional, Generator

from game_map.tiles.tile_layers.abstract_tile_layer import TileLayer
from game_map.tiles.tiles import BasicTile

class TileBlueprint:
    
    def get_layers(self, tile: BasicTile)->Optional[Generator[TileLayer, None, None]]:

        raise NotImplementedError