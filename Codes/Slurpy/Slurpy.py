import regex as re

# regular expression
reSlump = re.compile("([D|E]F+G*)+G")
reSlimp =  re.compile("AH|A([D|E]F+G*)+GC|AB(?R)C")

# test slurpy
def testSlurpy(testCase):
    m = re.match(reSlimp, testCase)
    if m:
        postFix = testCase[len(m.group()):]
        return re.fullmatch(reSlump, postFix) != None
    else:
        return False

# TestCase
testSlumps = "DFG", "EFG", "DFFFFFG", "DFDFDFDFG", "DFEFFFFFG"
testNotSlumps = "DFEFF", "EFAHG", "DEFG", "DG", "EFFFFDG"
testSlimps = "AH", "ABAHC", "ABABAHCC", "ADFGC", "ADFFFFGC", "ABAEFGCC", "ADFDFGC"
testNotSlimps = "ABC", "ABAH", "DFGC", "ABABAHC", "SLIMP", "ADGC"
testSlurpys = "AHDFG", "ADFGCDFFFFFG", "ABAEFGCCDFEFFFFFG"
testNotSlurpys = "AHDFGA", "DFGAH", "ABABCC"
print("testSlumps :", all([re.fullmatch(reSlump, testCase) != None for testCase in testSlumps]), testSlumps)
print("testNotSlumps :", all([re.fullmatch(reSlump, testCase) == None for testCase in testNotSlumps]), testNotSlumps)
print("testSlimps :", all([re.fullmatch(reSlimp, testCase) != None for testCase in testSlimps]), testSlimps)
print("testNotSlimps :", all([re.fullmatch(reSlimp, testCase) == None for testCase in testNotSlimps]), testNotSlimps)
print("testSlurpys :", all([testSlurpy(testCase) for testCase in testSlurpys]), testSlurpys)
print("testNotSlurpys :", all([not testSlurpy(testCase) for testCase in testNotSlurpys]), testNotSlurpys)
print("-"*50)

if __name__ == "__main__":
    n = input("input test count : ")
    testCases = [input("Test case " + str(i+1) + " : ").upper() for i in range(int(n))]
    print("-"*50)
    print("SLURPYS OUTPUT")
    for testCase in testCases:
        print("YES" if testSlurpy(testCase) else "NO")
    print("END OF OUTPUT")