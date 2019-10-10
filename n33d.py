from math import *

true = True
false = False
none = None


def to_radians(val: float) -> float:
    return val / 180 * pi


def to_degrees(val: float) -> float:
    return val / pi * 180


def get_sign(val: float or int) -> int:
    return -1 if val < 0 else 1 if val > 0 else 0


def nothing(*args, **kwargs):
    pass


def reduce_fraction(num: int, denom: int) -> (int, int):
    g = gcd(num, denom)
    return num // g, denom // g


def c(n: int, k: int) -> int:
    return factorial(n) // factorial(k) // factorial(n - k)


def a(n: int, k: int) -> int:
    return factorial(n) // factorial(n - k)


def rotate_point(x: float or int, y: float or int, angle: float, x0=0, y0=0) -> (int, int):
    return x0 + (x - x0) * cos(angle) - (y - y0) * sin(angle), y0 + (y - y0) * cos(angle) + (x - x0) * sin(angle)
