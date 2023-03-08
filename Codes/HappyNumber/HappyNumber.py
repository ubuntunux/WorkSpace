# find happy number
def is_happy_num(s0, history=[]):
    s1 = sum(map(lambda x:x*x, [int(i) for i in repr(s0)]))    
    if s1 == 1:
        return True
    elif s1 in history:
        return False
    else:
        history.append(s1)
        return is_happy_num(s1)

# Test case
for i, num in enumerate([3,7,4,13]):
    case = "Case #%d: %d is " % (i, num)
    result = "Happy number." if is_happy_num(num, []) else "an Unhappy number."
    print(case + result)