from itertools import product

from game_map.area.area import Area, Point
from game_map.area.tiles.tiles import BasicTile


def test_area():

    left_bottom = Point(0, 0)
    right_top = Point(10, 8)

    area = Area(left_bottom, right_top)

    assert area.center == Point(5, 4)
    assert area.size_x == 8
    assert area.size_y == 10


def test_tile_getting():

    left_bottom = Point(0, 0)
    right_top = Point(10, 10)
    area = Area(left_bottom, right_top)

    for y, x in product(range(10), range(10)):
        tile = BasicTile(y, x)
        area.add_object(tile)

    for y, x in product(range(10), range(10)):
        tile = area.get_object(y, x)
        point = Point(y, x)
        assert tile.bottom_left == point, f'{point=}, {tile=}'
