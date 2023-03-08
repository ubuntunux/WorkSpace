material = ('   ', ' - ', '|  ', '| |', '  |')
numToDigit = {}
numToDigit[0] = 1, 3, 0, 3, 1
numToDigit[1] = 0, 4, 0, 4, 0
numToDigit[2] = 1, 4, 1, 2, 1
numToDigit[3] = 1, 4, 1, 4, 1
numToDigit[4] = 0, 4, 1, 4, 0
numToDigit[5] = 1, 2, 1, 4, 1
numToDigit[6] = 1, 2, 1, 3, 1
numToDigit[7] = 1, 4, 0, 4, 0
numToDigit[8] = 1, 3, 1, 3, 1
numToDigit[9] = 1, 3, 1, 4, 0

def showDigit(size, num):
    digitNum = [int(n) for n in str(num)]
    for i in range(5):
        results = []
        for digit in digitNum:
            n = numToDigit[digit][i]
            results.append(material[n][0] + material[n][1] * size + material[n][2])
        print("\n".join([' '.join(results)] * (1 if i % 2 == 0 else size)))
            
# Run
showDigit(2, 12345)
showDigit(3, 67890)
showDigit(0, 0)