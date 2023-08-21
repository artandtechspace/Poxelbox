from typing import Generic, TypeVar

T = TypeVar("T")


class Vector2D(Generic[T]):
    x: T
    y: T

    def __init__(self, x: T, y: T):
        self.x = x
        self.y = y

    def __getitem__(self, key):
        if key < 0 or key > 1:
            raise Exception("Vector out of bounce")

        return self.x if key == 0 else self.y

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise Exception("Vector out of bounce")

    def __str__(self):
        return "( " + str(self.x) + ", " + str(self.y) + ")"

    def __bool__(self):
        return hasattr(self, 'x') and hasattr(self, 'y')

    def __eq__(self, other_vec):
        return other_vec.x == self.x and other_vec.y == self.y

    def __add__(self, other_vec):
        return Vector2D(self.x + other_vec.x, self.y + other_vec.y)

    def __sub__(self, other_vec):
        return Vector2D(self.x - other_vec.x, self.y - other_vec.y)

    def __mul__(self, other_vec):
        return Vector2D(self.x * other_vec.x, self.y * other_vec.y)

    def copy(self):
        return Vector2D(self.x, self.y)

    def copy_and_add(self, x: int = 0, y: int = 0):
        """Copies to vector and adds the given positions to it"""
        return Vector2D(self.x+x, self.y+y)
