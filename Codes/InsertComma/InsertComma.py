def split3(testCase):
    return (split3(testCase[:-3]) + "," + testCase[-3:]) if len(testCase) > 3 else testCase

testCase = input("Input test case : ")
sign = ""
if "-" == testCase[0]:
    sign = testCase[0]
    testCase = testCase[1:]
testCase, rest = testCase.split(".")
print(sign + ".".join([split3(testCase),rest]))
