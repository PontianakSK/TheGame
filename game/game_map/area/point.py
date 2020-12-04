from typing import Any


class Point:

    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

    def __add__(self, other: 'Point') -> 'Point':

        result = Point(self.y + other.y, self.x + other.x)

        return result

    def __sub__(self, other: 'Point') -> 'Point':

        result = Point(self.y - other.y, self.x - other.x)

        return result

    def __eq__(self, other: Any) -> bool:

        try:
            result = all([self.y == other.y, self.x == other.x])
        except AttributeError:
            result = False

        return result

    def __mul__(self, other: int) -> 'Point':

        result = Point(self.y * other, self.x * other)

        return result

    def __truediv__(self, other: int) -> 'Point':

        result = Point(round(self.y / other), round(self.x / other))

        return result

    def __repr__(self):

        result = f'Point ({id(self)}: {self.y=}, {self.x=})'

        return result
