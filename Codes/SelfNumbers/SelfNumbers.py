generate = lambda n : n + sum([int(x) for x in str(n)])
print(sum(set(range(1, 5000)) - set([generate(x) for x in range(1, 5000)])))