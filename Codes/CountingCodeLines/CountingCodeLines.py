import re

testCase = '''/*****
 * This is a test program with 5 lines of code
 *  \/* no nesting allowed!
//*****//***/// Slightly pathological comment ending...
public class Hello {
    public static final void main(String [] args) { // gotta love Java
        // Say hello
        System./*wait*/out./*for*/println/*it*/("Hello/*");
    }
}'''

testCase = re.sub("(?s)/\*.*?\*/", "", testCase)
print(len([True for line in testCase.split("\n") if not line.strip().startswith("//")]))
