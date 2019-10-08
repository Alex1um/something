def x_to_crds(x):
    global default, strs
    return x + sum(map(len, strs[:x]))


def move_line(x, y, li):
    global default, strs
    x = x_to_crds(x)
    p = -1
    if x > len(strs[y + li]):
        return len(strs[y + li]) - 1
    for i in strs[y + li]:
        if p <= x <= x_to_crds(i):
            return min(p, i, key=lambda z: abs(x_to_crds(z) - x))
        p = i


n, m = map(int, input().split())
default = tuple(input() for _ in ' ' * n)
strs = tuple(map(str.split, default))
li, w = (lambda x: (int(x[0]), strs.index(x[1])))(input().split())
x, y = 0, 0
way = float('inf')
ways = 0
while x != w and y != li:
    if abs(move_line(x, y, 1) - w) < abs(x - w) or move_line(x, y, 1) == li:
        x = move_line(x, y, 1)
        y += 1
        ways += 1
    elif abs(move_line(x, y, -1) - w) < abs(x - w) or move_line(x, y, -1) == li:
        x = move_line(x, y, -1)
        y -= 1
        ways += 1
    else:
        x += 1 if x < w else -1