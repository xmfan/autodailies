from dataclasses import dataclass

@dataclass
class Coordinate:
    x: int
    y: int

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coordinate(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Coordinate(self.x * scalar, self.y * scalar)

    def asTuple(self):
        return (self.x, self.y)

