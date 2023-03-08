def genPalindrome():
    n = 0
    while True:
        digit = str(n)
        for i in range(len(digit)):
            if digit[i] != digit[-(i+1)]:
                break
        else:
            yield n
        n += 1
    
n = input("input : ")
n = int(n)
lastPalindrome = 0
p = genPalindrome()

for i in range(n):
    lastPalindrome = p.next()
print(lastPalindrome)

