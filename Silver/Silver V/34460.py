i = int(input())
for t in range(i):
    l, s = int(input()), list(input())
    it = -1
    for r in range(l):
        if s[r] == "M":
            if (it == -1) or (it == 2): it = 0
            else: it = -2
        elif s[r] == "I":
            if (it == 0) or (it == 2): it = 1
            else: it = -2
        elif s[r] == "T":
            if it == 1: it = 2
            else: it = -2
        else: it = -2
    if it == 2: print("YES")
    else: print("NO")