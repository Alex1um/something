import numpy as np

with open('input.bmp', 'rb') as f:
    s1 = f.read()
    s = np.array(np.frombuffer(s1[54:], np.uint8, -1))
with open('res.bmp', 'wb') as f:
    f.write(s1[:54] + (255 - s).tobytes())
#
# with open('input.bmp', 'rb') as f:
#     s = f.read()
# new = s[:54]
# for i in s[54:]:
#     new += (255 - i).to_bytes(1, 'little')
# with open('res.bmp', 'wb') as f:
#     f.write(new)
