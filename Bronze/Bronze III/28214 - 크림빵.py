i = input()
n, k, p = int(i.split()[0]), int(i.split()[1]), int(i.split()[2])
b = input().split()

s = 0
for t in range(n):
    e = 0
    for h in range(k):
        a = (t * k) + h
        if b[a] == '0': e += 1
    if e < p: s += 1
print(s)