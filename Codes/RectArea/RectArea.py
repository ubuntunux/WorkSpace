'''
Python으로 작성했습니다. 면적에 해당하는 좌표를 리스트에 집어넣고 중복되는 영역은 무시하고 리스트 원소의 갯수를 센다.
'''

def getArea(rects):
    pointList = set()
    for rect in rects:
        for x in range(rect[0], rect[2]):
            for y in range(rect[1], rect[3]
        pointList.add((x,y))
    return len(pointList)

rects=[]
print("Input rectangle 4 points or enter for quit")
while True:
    v = input()
    if v == "":
        break
    else:
        rects.append([int(x) for x in v.split(" ")])
print("area : %d" % getArea(rects))
