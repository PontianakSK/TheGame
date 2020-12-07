from typing import Callable, List

from game_map.area.tiles.tiles import BasicTile
import game_map.area.tiles.tile_layers.tile_layers as tile_layers


class TileBuilder:

    def __init__(self):

        # defines TileLayers depanding on tile's height.
        self._layer_height_thresholds = [
            (0.7, tile_layers.SoilLayer),
            (0.4, tile_layers.SandLayer),
            (0.3, tile_layers.WaterLayer),
        ]
        self._deepest_layer = tile_layers.StoneLayer

    def build(self, y: int, x: int, height: float) -> BasicTile:
        '''
        Creates Tile and filles with layers depending on tile's
        height.
        '''

        tile = BasicTile(y, x, height)
        layers = []
        for threshhold, layer in self._layer_height_thresholds:
            if threshhold >= height:
                layers.append(layer)

        top_layer = self._chain_layers(layers)
        tile.add_object(top_layer)

        return tile

    def _chain_layers(self, layers: List[Callable]) -> tile_layers.TileLayer:
        '''
        Creates layers one by one and adds previously created inside.
        '''

        current_layer = self._deepest_layer()

        for layer in layers:
            current_layer = layer(current_layer)

        return current_layer
