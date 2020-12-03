from game_map.interactive_object import InteractiveObject  # type: ignore
from game_map.area.point import Point  # type: ignore


class Area(InteractiveObject):

    def __init__(self, bottom_left: Point, top_right: Point):

        super().__init__()
        self.bottom_left = bottom_left
        self.top_right = top_right

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
