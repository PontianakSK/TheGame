from itertools import product
from typing import Tuple

from game_map.area.area_fillers.area_filler import AreaFiller, Area
from game_map.area.height_gens.abstract_gen import TileHeightGenerator
from game_map.area.tiles.tile_builders import TileBuilder, BasicTile


class HeightFiller(AreaFiller):
    '''
    Filles Area with Tiles depending on height of tile.
    TileHeightGenerator is responsible for determining
    tile's height based on coordinates.
    TileBuilder fills tile with tile layers and other
    objects.
    '''

    def __init__(self, height_gen: TileHeightGenerator, builder: TileBuilder):

        self._height_gen = height_gen
        self._builder = builder

    def fill(self, area: Area) -> Area:
        '''
        Fills Area with tiles and returns the Area
        '''

        size_x = area.size_x
        size_y = area.size_y

        for y, x in product(range(size_y), range(size_x)):
            y_perc, x_perc = self._get_perc_coords(y, x, area)
            height = self._get_height(y_perc, x_perc)
            tile = self._build_tile(y, x, height)
            area.add_object(tile)

        return area

    def _get_perc_coords(self, y: int, x: int, area: Area) -> Tuple[float]:
        '''
        Height generators uses only relative coordinates from 0 to 1.
        Where 0 means start of axis and 1 means end of map (0+size_*)
        '''

        scale = max(area.size_x, area.size_y)
        result = (y/scale, x/scale)

        return result

    def _get_height(self, y_perc: int, x_perc: int) -> float:
        '''
        Returns height from TileHeightGenerator.
        '''

        result = self._height_gen.get_height(y_perc, x_perc)

        return result

    def _build_tile(self, y: int, x: int, height: float) -> BasicTile:
        '''
        Returns tile created by TileBuilder
        '''

        tile = self._builder.build(y, x, height)

        return tile
