n = int(input())

a = ""
p = {}
m = {}
for i in range(n):
    s = input().split()
    p[i] = [s, 0]
    for g in range(len(s)): m[s[g]] = i
    a += (' '.join(s) + ' ')

w = a.split()
l = input().split()

c = True
for t in range(len(l)):
    a = l[t]
    if a in w:
        w.remove(a)
        b = m[a]
        if p[b][0][p[b][1]] == a: p[b][1] = p[b][1] + 1
        else: c = False; break
    else: c = False; break

if c == False: print("Impossible")
elif w == []: print("Possible")
else: print("Impossible")