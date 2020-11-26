from game_map.tiles.tiles import BasicTile
from game_map.tiles.tile_blueprints.abstract_tile_blueprint import TileBlueprint

class AbstractTileBuilder:

    def __init__(self, blueprint: TileBlueprint):
        self.blueprint = blueprint

    def build(self, params: dict)->BasicTile:
        raise NotImplementedError


class HeightBuilder(AbstractTileBuilder):
    
    def build(self, params: dict)->BasicTile:
        
        height = params.get('height')

        if height is not None:
            tile = BasicTile(height)
            layers = self.blueprint.get_layers(tile)
            current_layer = None

            for layer in layers:
                current_layer = layer(lower_layer=current_layer)

            tile.top_layer = current_layer
            
            return tile

        raise ValueError('Height should be in params')


