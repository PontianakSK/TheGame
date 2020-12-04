import pytest

from game_map.area.tiles.tiles import (
    BasicTile,
    Point,
    TileLayer,
    InteractiveObject,
)


def test_tile_creation():

    tile = BasicTile(0, 1, 2)
    assert tile.bottom_left == Point(0, 1)
    assert tile.top_right == Point(1, 2)
    assert tile._height == 2


def test_adding_objects():

    tile = BasicTile(0, 0)
    first_layer = TileLayer()
    second_layer = TileLayer()
    inter_object = InteractiveObject()

    tile.add_object(inter_object)
    assert inter_object in tile.container

    tile.add_object(first_layer)
    assert tile.top_layer == first_layer

    error = InteractiveObject.AddingObjectError

    with pytest.raises(error) as exc_info:
        tile.add_object(second_layer)

    error_message = 'Only one internal TileLayer is allowed'
    assert error_message in str(exc_info.value)
