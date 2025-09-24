n = int(input())
for t in range(n):
  i = input()
  c, v = int(i.split()[0]), int(i.split()[1])
  print(f"You get {c // v} piece(s) and your dad gets {c % v} piece(s).")
