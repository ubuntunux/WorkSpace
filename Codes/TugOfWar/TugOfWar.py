'''
** 나의 문제 풀이 방법 **
가장먼저 할일은 팀원을 배정받은 후에 팀인원이 홀수인 경우 몸무게가 0인 가상의 팀원을 하나 배열에 추가하여 짝이 맞도록 한다.
우선 팀원중 아무나 한명을 선발하고 남아있는 팀원들중 몸무게 차이가 가장 적게나는 사람을 선발한다.
둘의 몸무게를 비교하여 몸무게가 많이 나가는 사람을 현재까지 몸무게 총합이 적은팀으로 보내고
몸무게가 적게 나가는 사람을 현재까지 몸무게 총합이 큰팀으로 보내어 균형을 맞춘다
남아있는 사람이 없을때 까지 이것을 반복한다. 
각 개인의 몸무게 차이가 가장 적은 사람들끼리 팀을 나누면 결과적으로 팀간의 몸무게차가 최소가 되는 원리이다.
'''

def balance(weights, left, right):
    weight = weights.pop()
    # find closed number with weight
    closedValue = min([(999, 0)] + [(abs(weight-x), x) for x in weights])[1]
    weights.remove(closedValue)
    if left > right:
        left += min(weight, closedValue)
        right += max(weight, closedValue)
    else:
        left += max(weight, closedValue)
        right += min(weight, closedValue)
    if len(weights) != 0:
        return balance(weights, left, right)    
    return (left, right) if left < right else (right, left)

while True:
  # input count and weights
  count = int(input("Input Count : "))
  array = []
  for x in range(count):
    array.append(max(1, min(450, int(input("%d. Input weight : " % (x+1))))))
  # make even length
  if len(array) % 2 == 1:
      array.append(0)
  # show result
  print("Result : %d %d\n" % balance(array, 0, 0))
