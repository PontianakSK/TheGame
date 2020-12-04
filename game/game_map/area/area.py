from typing import Optional

from game_map.interactive_object import InteractiveObject  # type: ignore
from game_map.area.point import Point  # type: ignore


class Area(InteractiveObject):

    def __init__(self, bottom_left: Point, top_right: Point):

        super().__init__()
        self.bottom_left = bottom_left
        self.top_right = top_right

    def get_object(self, y: int, x: int) -> Optional[InteractiveObject]:

        index_ = y * self.size_x + x

        try:
            result = self.container[index_]
        except IndexError:
            return None

        return result

    @property
    def center(self) -> Point:

        result = (self.bottom_left + self.top_right)/2

        return result

    @property
    def size_x(self) -> int:

        result = self.top_right.x - self.bottom_left.x

        return result

    @property
    def size_y(self) -> int:

        result = self.top_right.y - self.bottom_left.y

        return result
