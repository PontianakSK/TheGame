import pytest

from game_map.game_map import GameMap
from game_map.area.tiles.tiles import BasicTile
from game_map.interactive_object import InteractiveObject


def test_singleton() -> None:

    size_y, size_x = 100, 100
    first_instace = GameMap(size_y, size_x)
    second_instance = GameMap(size_y, size_x)
    assert first_instace is second_instance


def test_adding_tiles() -> None:

    size_y, size_x = 100, 100
    game_map = GameMap(size_y, size_x)
    tile = BasicTile(20, 20)
    other_object = InteractiveObject()
    game_map.add_object(tile)
    assert tile in game_map.container

    with pytest.raises(InteractiveObject.AddingObjectError) as exc_info:
        game_map.add_object(other_object)
    error_message = 'Map should contains BasicTiles only!'
    assert error_message in str(exc_info.value)
