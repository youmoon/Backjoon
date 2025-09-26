i = input()
n, k, a = int(i.split()[0]), int(i.split()[1]), []
for t in range(k): a.append(int(str(n * (t + 1))[::-1]))
print(max(a))
