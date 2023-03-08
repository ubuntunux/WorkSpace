#-*-coding:utf-8-*-
DEBUG = False
checkPattern = [(0, -1), (-1, 0), (1, 0), (0, 1)]
checkedFlag = "o"

def checkNode(datas, x, y):
    datas[y][x] = checkedFlag
    for pattern in checkPattern:
        coord = (x + pattern[0], y + pattern[1])
        if (0 <= coord[1] < len(datas)) and (0 <= coord[0] < len(datas[coord[1]])):
            data = datas[coord[1]][coord[0]]
            #### DEBUG START
            if DEBUG:
                print("")
                datas[y][x] = "*"
                datas[coord[1]][coord[0]] = "?"
                for line in datas:
                    print("".join(line))
                datas[y][x] = checkedFlag
                datas[coord[1]][coord[0]] = checkedFlag
            #### END OF DEBUG
            if data != checkedFlag:                
                if data == ">": 
                    print("Found '>' at", coord)
                    return True
                elif data == " ":
                    # recursive search
                    if checkNode(datas, coord[0], coord[1]):
                        return True
    return False

def isPossible(data):
    # 문자열 형태인 data를 리스트로 변환
    datas = [list(line) for line in data.split("\n")]    
    # 시작지점 "<"의 위치를 찾는다.
    sX, sY = 0, 0
    for y in range(len(datas)):
        if "<" in datas[y]:
            sX, sY = datas[y].index("<"), y
    # 찾기시작          
    if not checkNode(datas, sX, sY):
        print("Not found.")
        
#-------------------#
# Test
#-------------------#
data1="""<     >"""

data2="""########
#<     #
#  ##  #
#  ##  #
#     >#
########"""

data3="""#######
#<    #
##### #
#     #
# #####
# #   #
# # # #
#   #>#
#######"""

data4="""<   #   >"""

data5 = """########
#<     #
#     ##
#    #>#
########"""

data6 = """#< #  #
#  #  #
#  # >#"""

isPossible(data1)
isPossible(data2)
isPossible(data3)
isPossible(data4)
isPossible(data5)
isPossible(data6)
