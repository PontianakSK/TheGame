from game_map.tiles.tile_blueprints import basic_height_blueprint
from game_map.tiles.tile_layers.abstract_tile_layer import TileLayer
from game_map.tiles.tiles import BasicTile


def test_interface():

    blueprint = basic_height_blueprint.BasicHeightBlueprint()
    min_threshold = float(min(blueprint._height_thresholds.keys()))
    max_threshold = float(max(blueprint._height_thresholds.keys()))
    delta = max_threshold-min_threshold
    cases = [min_threshold+delta*(i/10) for i in range(0, 11)]
    cases.extend([-100, 100])

    for case in cases:
        tile = BasicTile(case)
        layers = blueprint.get_objects(tile)
        layer = next(layers)
        assert issubclass(layer, TileLayer), f'{case=}'


def test_get_objects():

    blueprint = basic_height_blueprint.BasicHeightBlueprint()
    thresholds = blueprint._height_thresholds.keys()

    for threshold in thresholds:
        tile = BasicTile(threshold)
        layer_gen = blueprint.get_objects(tile)
        blueprint_layers = blueprint._height_thresholds[threshold]

        for layer in layer_gen:
            assert layer in blueprint_layers, f'{threshold=}'


def test_deepest_layers():

    blueprint = basic_height_blueprint.BasicHeightBlueprint()
    height = -100
    tile = BasicTile(height)
    layer_gen = blueprint.get_objects(tile)

    for layer in layer_gen:
        assert layer in blueprint._deepest_layers, f'{layer=}'
