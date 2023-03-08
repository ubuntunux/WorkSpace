S = [1, 3, 4, 8, 13, 17, 20] 
pairs = zip(S[:-1], S[1:])
print(sorted(pairs, key=lambda pair:abs(pair[0]-pair[1]))[0])

