def findCommonString(s, lowerLengthString):
    if len(lowerLengthString) > len(s):
        s, lowerLengthString = lowerLengthString, s

    n = len(lowerLengthString)
    for i in range(n):
        for j in range(i+1):
            token = lowerLengthString[j:n-i+j]
            if token in s:
                print(len(token))
                print(token)
                return
    else:
        print("Not found.")

# let's find common string.
findCommonString("photography", "autograph")
