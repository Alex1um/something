from functools import reduce

n, k = map(int, input().split())
d = {'A': 1, 'B': 0, 'C': -1}
print(abs(sum(i for i in reduce(lambda x, y: x + [x[-1] + d[y]], input(), [k]) if i < 0)))