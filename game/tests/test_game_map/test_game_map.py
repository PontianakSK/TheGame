import pytest

from game_map.game_map import GameMap, Point
from game_map.area.tiles.tiles import BasicTile
from game_map.interactive_object import InteractiveObject


def test_singleton() -> None:

    bottom_left = Point(0, 0)
    top_right = Point(100, 100)
    first_instace = GameMap(bottom_left, top_right)
    second_instance = GameMap(bottom_left, top_right)
    assert first_instace is second_instance


def test_adding_tiles() -> None:

    bottom_left = Point(0, 0)
    top_right = Point(100, 100)
    game_map = GameMap(bottom_left, top_right)
    tile = BasicTile(20, 20)
    other_object = InteractiveObject()
    game_map.add_object(tile)
    assert tile in game_map.container

    with pytest.raises(InteractiveObject.AddingObjectError) as exc_info:
        game_map.add_object(other_object)
    error_message = 'Map should contains BasicTiles only!'
    assert error_message in str(exc_info.value)
