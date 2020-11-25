from typing import Generator, Optional

from game_map.tiles.tile_blueprints.abstract_tile_blueprint import TileBlueprint
from game_map.tiles.tiles import BasicTile
from game_map.tiles.tile_layers.abstract_tile_layer import TileLayer
from game_map.tiles.tile_layers.tile_layers import WaterLayer, SandLayer, SoilLayer, StoneLayer, GrassLayer

class BasicHeightBlueprint(TileBlueprint):



    def __init__(self):
        self._height_thresholds = {
            0.9: [StoneLayer, StoneLayer, WaterLayer,StoneLayer],
            0.6: [SoilLayer, SandLayer, WaterLayer, StoneLayer],
            0.4: [GrassLayer, SoilLayer, SandLayer, WaterLayer, StoneLayer],
            0.3: [SandLayer, StoneLayer],
            0.2: [WaterLayer, SandLayer, StoneLayer],
            0: [WaterLayer,WaterLayer,StoneLayer],
        }
        self._deepest_layers = [WaterLayer,WaterLayer,WaterLayer] 


    def get_layers(self, tile: BasicTile)->Optional[Generator[TileLayer, None, None]]:

        height = tile.height

        for threshold in self._height_thresholds:

            if height >= threshold:
                return (layer for layer in self._height_thresholds[threshold][::-1])

        return (layer for layer in self._deepest_layers[::-1])
            