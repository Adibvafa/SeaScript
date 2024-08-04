from math import sqrt, inf
import random as rand

class Vec2d:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vec2d(self.x * other, self.y * other)

    def __truediv__(self, other):
        return Vec2d(self.x / other, self.y / other)

    def __floordiv__(self, other):
        return Vec2d(self.x // other, self.y // other)

    def __mod__(self, other):
        return Vec2d(self.x % other, self.y % other)


    def length_squared(self):
        return self.x ** 2 + self.y ** 2

    def normalize(self):
        length = sqrt(self.length_squared())
        if length == 0:
            raise ValueError("Zero length vector cannot be normalized")
        return Vec2d(self.x / length, self.y / length)

    def coerce_in(self, min_val, max_val):
        return max(min_val, min(self, max_val))

    def __repr__(self):
        return f"Vec2d({self.x}, {self.y})"

    def contained_within(self, min_vec, max_vec):
        return (min_vec.x <= self.x <= max_vec.x and
                min_vec.y <= self.y <= max_vec.y)

    def __sub__(self, other):
        return Vec2d(self.x - other.x, self.y - other.y)


class Box2d:
    def __init__(self, position: Vec2d, dimensions: Vec2d):
        self.min = position
        self.max = position + dimensions

    @classmethod
    def from_coordinates(cls, x: float, y: float, dx: float, dy: float):
        return cls(Vec2d(x, y), Vec2d(dx, dy))

    def collides_1d(self, min1: float, max1: float, min2: float, max2: float) -> bool:
        return max1 >= min2 and min1 <= max2

    def intersection_1d(self, min1: float, max1: float, min2: float, max2: float):
        min_val = max(min1, min2)
        max_val = min(max1, max2)
        if min_val > max_val:
            return None
        return min_val, max_val

    def contains(self, point: Vec2d) -> bool:
        return point.contained_within(self.min, self.max)

    def collides(self, other: 'Box2d') -> bool:
        return (self.collides_1d(self.min.x, self.max.x, other.min.x, other.max.x) and
                self.collides_1d(self.min.y, self.max.y, other.min.y, other.max.y))

    def distance(self, point: Vec2d) -> float:
        dx = max(max(self.min.x - point.x, 0.0), point.x - self.max.x)
        dy = max(max(self.min.y - point.y, 0.0), point.y - self.max.y)
        distance = sqrt(dx ** 2 + dy ** 2)
        return -distance if self.contains(point) else distance

    def constrained_collision_time_1d(self, min1: float, max1: float, min2: float, max2: float, slide: float):
        collision_time = self.collision_time_1d(min1, max1, min2, max2, slide)
        if collision_time is None:
            return None
        min_t, max_t = collision_time
        if min_t > 1.0 or max_t < 0.0:
            return None
        return min_t, max_t

    def collision_time_1d(self, min1: float, max1: float, min2: float, max2: float, slide: float):
        if slide == 0.0:
            if self.collides_1d(min1, max1, min2, max2):
                return 0.0, inf
            return None
        t1 = (min2 - max1) / slide
        t2 = (max2 - min1) / slide
        return min(t1, t2), max(t1, t2)

    def collision_time(self, other: 'Box2d', slide: Vec2d) -> (bool, float):
        if self.collides(other):
            return True, 0.0

        col_time_x = self.constrained_collision_time_1d(self.min.x, self.max.x, other.min.x, other.max.x, slide.x)
        if col_time_x is None:
            return False, 0.0
        col_time_y = self.constrained_collision_time_1d(self.min.y, self.max.y, other.min.y, other.max.y, slide.y)
        if col_time_y is None:
            return False, 0.0

        col_xy = self.intersection_1d(col_time_x[0], col_time_x[1], col_time_y[0], col_time_y[1])
        if col_xy is None:
            return False, 0.0

        return True, col_xy[0]

    def intersection(self, ray_origin: Vec2d, ray_direction: Vec2d):
        if ray_direction.length_squared() == 0.0:
            raise ValueError("Ray direction cannot be zero")

        normalized_ray_direction = ray_direction.normalize()

        intersection_time_x = self.collision_time_1d(ray_origin.x, ray_origin.x, self.min.x, self.max.x,
                                                     normalized_ray_direction.x)
        intersection_time_y = self.collision_time_1d(ray_origin.y, ray_origin.y, self.min.y, self.max.y,
                                                     normalized_ray_direction.y)

        if intersection_time_x is None or intersection_time_y is None:
            return False, None

        intersection_time_xy = self.intersection_1d(intersection_time_x[0], intersection_time_x[1],
                                                    intersection_time_y[0], intersection_time_y[1])
        if intersection_time_xy is None:
            return False, None

        return True, intersection_time_xy

    def clamp(self, point: Vec2d) -> Vec2d:
        return Vec2d(
            max(self.min.x, min(point.x, self.max.x)),
            max(self.min.y, min(point.y, self.max.y))
        )

    def random_point(self) -> Vec2d:
        return Vec2d(
            rand.uniform(self.min.x, self.max.x),
            rand.uniform(self.min.y, self.max.y)
        )

    def __repr__(self):
        return f"Box2d(position={self.min}, min={self.min}, max={self.max})"
