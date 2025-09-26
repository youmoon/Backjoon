i = input()
n, k, h = int(i.split()[0]), int(i.split()[0]), 0
for t in range(k):
    if int(str(n * (t + 1))[::-1]) > h: h = int(str(n * t)[::-1])
print(h)
