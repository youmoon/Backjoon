n = int(input())
for t in range(n):
  i = input()
  c, v = e.split()[0], e.split()[1]
  print(f"You get {c // v} piece(s) and your dad gets {c % v} piece(s).")
