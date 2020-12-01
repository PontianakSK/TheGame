from game_map.tiles.tiles import BasicTile
from game_map.intaractive_object_creator import InteractiveObjectCreator


class HeightBuilder(InteractiveObjectCreator):

    def build(self, params: dict) -> BasicTile:

        height = params.get('height')

        if height is not None:
            tile = BasicTile(height)
            layers = self.blueprint.get_objects(tile)
            current_layer = None

            for layer in layers:
                current_layer = layer(lower_layer=current_layer)

            tile.add_object(current_layer)

            return tile

        raise ValueError('Height should be in params')
