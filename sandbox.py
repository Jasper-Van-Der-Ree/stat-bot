from collections import deque

x = range(10)

i = iter(x)
d = deque(i)
print(len(d))

