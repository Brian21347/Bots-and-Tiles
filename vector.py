from typing import Union


vector2d_like = Union['Vector2d', list[int | float, int | float], tuple[int | float, int | float]]


class Vector2d:
    def __init__(self, x: int | float, y: int | float):
        self.x = x
        self.y = y

    @property
    def normalized(self):
        return Vector2d(self.x / self.magnitude, self.y / self.magnitude)

    @property
    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** .5

    def __add__(self, other: vector2d_like) -> 'Vector2d':
        if isinstance(other, Vector2d):
            return Vector2d(self.x + other.x, self.y + other.y)
        else:
            return Vector2d(self.x + other[0], self.y + other[1])

    def __iadd__(self, other: vector2d_like) -> 'Vector2d':
        return self + other

    def __mul__(self, other: int | float):
        return Vector2d(self.x*other, self.y *other)

    def __imul__(self, other: int | float):
        return self * other

    def __neg__(self):
        return self * -1

    def __sub__(self, other: vector2d_like):
        return self + other * -1

    def __isub__(self, other: vector2d_like):
        return self - other

    def __len__(self):
        return 2

    def __iter__(self):
        yield self.x
        yield self.y
