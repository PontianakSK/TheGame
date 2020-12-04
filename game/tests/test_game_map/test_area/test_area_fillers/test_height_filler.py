from itertools import product

from game_map.area.area_fillers.height_filler import HeightFiller
from game_map.area.area import Area
from game_map.area.point import Point
from game_map.area.tiles.tile_builders import TileBuilder, tile_layers
from game_map.area.height_gens.abstract_gen import TileHeightGenerator


class TestGen(TileHeightGenerator):

    def get_height(self, y_perc: float, x_perc: float):

        if y_perc >= x_perc:
            return 100
        return -100


def test_filler():

    builder = TileBuilder()
    height_gen = TestGen()
    filler = HeightFiller(height_gen, builder)
    left_bottom = Point(0, 0)
    right_top = Point(2, 2)
    area = Area(left_bottom, right_top)
    area = filler.fill(area)
    tiles = area.container

    for i, tile in enumerate(tiles):

        if i == 1:
            msg = f'{i=}, {tile=}'
            assert tile._height == -100, msg
            assert isinstance(tile.top_layer, tile_layers.WaterLayer), msg

        else:
            msg = f'{i=}, {tile=}'
            assert tile._height == 100, msg
            assert isinstance(tile.top_layer, tile_layers.StoneLayer), msg


def test_tile_coordinates():
    builder = TileBuilder()
    height_gen = TestGen()
    filler = HeightFiller(height_gen, builder)
    left_bottom = Point(0, 0)
    right_top = Point(2, 2)
    area = Area(left_bottom, right_top)
    area = filler.fill(area)

    for y, x in product(range(2), range(2)):
        tile = area.get_object(y, x)
        point = Point(y, x)
        assert tile.bottom_left == point, f'{point=}, {tile=}'
