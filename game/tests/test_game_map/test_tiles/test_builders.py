import pytest

from game_map.tiles import tile_builders
from game_map.tiles.tile_blueprints.basic_height_blueprint import (
    BasicHeightBlueprint
)
from game_map.tiles.tile_layers.abstract_tile_layer import TileLayer
from game_map.tiles.tiles import BasicTile


def test_height_builder_layers():

    blueprint = BasicHeightBlueprint()
    builder = tile_builders.HeightBuilder(blueprint)
    height = next(iter(blueprint._height_thresholds.keys()))
    layers = blueprint._height_thresholds[height]
    params = {
        'height': height,
    }
    tile = builder.build(params)
    next_tile_layer = tile.top_layer

    for layer in layers:
        assertion_message = f'{next_tile_layer=}, {layer=}'
        assert isinstance(next_tile_layer, layer), assertion_message
        next_tile_layer = next_tile_layer.lower_layer


def test_height_builder_inputs():

    blueprint = BasicHeightBlueprint()
    builder = tile_builders.HeightBuilder(blueprint)
    params = {}

    with pytest.raises(ValueError) as exc_info:
        builder.build(params)
    assertion_message = 'If "height" not in params, exception should be raised'
    assert 'Height should be in params' in str(exc_info.value), (
        assertion_message
    )

    for height in [-100, 0, 0.1, 0.5, 100]:
        params['height'] = height
        tile = builder.build(params)

        assert isinstance(tile, BasicTile), f'{height=}'

        next_layer = tile.top_layer

        while next_layer is not None:

            assert isinstance(next_layer, TileLayer), f'{height=}'

            next_layer = next_layer.lower_layer
