import time
# coding: utf-8
'''
bit flag를 이용한 문제 풀기
8칸인 경우 가로줄은 00000001, 00000010 ...... 10000000 중에 하나가 되며 1 bit만 True이기 때문에 가로로 겹치는 경우는 없기 때문에 가로 검사는 따로 하지 않아도 된다.
대각선과 세로로 겹치는지 검사하기만 하면 되는데 OR연산을 이용하여 leftMask(왼쪽대각선), righMask(오른쪽대각선), accMask(세로마스크) 들을 하나의 mask로 합친다.
ex) mask = FULL_BIT_FLAG & (accMask | leftMask | rightMask)
여기 현재의 값(q)와 mask를 AND연산했을때 0 이 나오면 겹치치 않으므로 Safe이다. 그러므로 결과를 저장한다.
'''

SIZE = 8
FULL_BIT_FLAG = (2**SIZE) - 1 # 8bit example => 11111111

def queens(accMask, leftMask, rightMask, acc_result, total_result):
    # mask - check for safe
    mask = FULL_BIT_FLAG & (accMask | leftMask | rightMask)
    for i in range(SIZE):
        # q is Queen
        q = 1 << i
        # safe case -  not overlap case
        if q & mask == 0:
            nextAccMask = accMask | q
            nextlLeftMask = (leftMask | q) << 1
            nextrRightMask = (rightMask | q) >> 1
            result = acc_result + [q]
            # problem solved
            if nextAccMask == FULL_BIT_FLAG:
                # record result to total result
                total_result.append(result)
                return
            else:
                queens(nextAccMask, nextlLeftMask, nextrRightMask, result, total_result)
    return total_result

# problem resolve
final_result = queens(0, 0, 0, [], [])

# show
for result in final_result:
    # number to bit flag string
    print("\n".join(["{0:b}".format(num).zfill(SIZE) for num in result]) + "\n")
        
print("Total answer count : %d" % len(final_result))