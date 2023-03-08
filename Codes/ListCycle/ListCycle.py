import collections
datas = input("Input : ").split(" ")
cycleList = collections.deque(datas[1:])
cycleList.rotate(int(datas[0]))
print("Output :", " ".join(cycleList))