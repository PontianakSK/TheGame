from typing import Optional

from game_map.interactive_object import InteractiveObject  # type: ignore
from game_map.area.point import Point  # type: ignore


class Area(InteractiveObject):
    '''
    For interactive objects that cannot be placed on one
    tile. Area is rectangular.
    '''

    def __init__(self, bottom_left: Point, top_right: Point):

        super().__init__()
        self.bottom_left = bottom_left
        self.top_right = top_right

    def get_object(self, y: int, x: int) -> Optional[InteractiveObject]:
        '''
        Returns object by coordinates. (objects are stored
        in flat list)
        '''

        index_ = y * self.size_x + x

        try:
            result = self.container[index_]
        except IndexError:
            return None

        return result

    @property
    def center(self) -> Point:
        '''
        Returns coordinates of tile in the center of
        area. Coordinates are rounded to the closest
        integer.
        '''

        result = (self.bottom_left + self.top_right)/2

        return result

    @property
    def size_x(self) -> int:
        '''
        X-axis length of the Area.
        '''

        result = self.top_right.x - self.bottom_left.x

        return result

    @property
    def size_y(self) -> int:
        '''
        Y-axis length of the Area
        '''

        result = self.top_right.y - self.bottom_left.y

        return result
