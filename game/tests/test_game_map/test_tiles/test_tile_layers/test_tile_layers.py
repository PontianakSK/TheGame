import pytest

from game_map.tiles.tile_layers import tile_layers
from game_map.interactive_object import InteractiveObject
from game_map.impact import Impact

TILE_LAYERS = [
    tile_layers.GrassLayer,
    tile_layers.SandLayer,
    tile_layers.SoilLayer,
    tile_layers.StoneLayer,
    tile_layers.WaterLayer,
]


def test_layers_hierarchy():

    for layer_class in TILE_LAYERS:

        inner_layer = layer_class()
        outer_layer = layer_class(inner_layer)

        assert outer_layer.lower_layer == inner_layer
        assert outer_layer.fertility == inner_layer.fertility


def test_lower_layer_uniqueness():

    for layer_class in TILE_LAYERS:

        inner_layer = layer_class()
        outer_layer = layer_class(inner_layer)
        excess_layer = layer_class()

        with pytest.raises(InteractiveObject.AddingObjectError) as excinfo:
            outer_layer.add_object(excess_layer)
        assert 'Only one internal TileLayer is allowed' in str(excinfo.value)


def test_impact_acceptance():

    for layer_class in TILE_LAYERS:

        impact = Impact()
        inner_layer = layer_class()
        outer_layer = layer_class(inner_layer)
        outer_layer.accept_impact(impact)
