from math import *

def isPerfectNumber(n):
    divisors = [1, ]
    for i in range(2, floor(sqrt(n)) + 1):
        if n % i == 0:
            divisors.append(i)
            divisors.append(int(n / i))
    return sum(divisors) == n

def main():
    perfectNumbers = []
    N = int(input("Input Number : "))    
    for i in range(1, N+1):
        if isPerfectNumber(i):
            perfectNumbers.append(i)
    if perfectNumbers:
        print("PerfectNumber :", perfectNumbers)
        
if __name__ == '__main__':
    main()
