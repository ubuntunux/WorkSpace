while True:
  A, B = input("Input 2 numsbers or 0 0 for quit : ").split()
  if A != "0" or B != "0":
    print("%d carry operation." % len([i for i in range(1, min(len(A), len(B))+1) if (int(A[-i:])+int(B[-i:])) >= 10**i]))
  else:
    break