import Text.Regex
import Text.Regex.Posix
import Control.Monad

-- REGULAR EXPRESSIONS
reSlump = makeRegex "([D|E]F+)+G"::Regex
reSlimp = makeRegex "AH|A([D|E]F+)+GC|AB(.+)C"::Regex

-- check functions
isMatched (Just (a,b,c,d)) = (a == "" && b /= "")
isMatched Nothing = False

isFullMatched (Just (a,b,c,d)) = (a == "" && b /= "" && c == "")
isFullMatched Nothing = False

getRecursiveSlimp (Just (a,b,c,d)) = if length d > 1 then d !! 1 else ""
getRecursiveSlimp Nothing = ""

restTestCase (Just (a,b,c,d)) = c
restTestCase Nothing = ""

-- test Slump, Slimp
test regex testCase = if matchedGroup /= "" then test regex matchedGroup else isMatched result
    where
        result = matchRegexAll regex testCase
        matchedGroup = getRecursiveSlimp result

-- test Slurpy
testSlurpy testCase = if isSlimp then isSlump else False
    where
        resultSlimp = matchRegexAll reSlimp testCase
        isSlimp = isMatched resultSlimp
        isSlump = isFullMatched $ matchRegexAll reSlump (restTestCase resultSlimp)


main = do
    -- test case
    let 
        testCaseSlumps = ["DFG", "EFG", "DFFFFFG", "DFDFDFDFG", "DFEFFFFFG"]
        testCaseNotSlumps = ["DFEFF", "EFAHG", "DEFG", "DG", "EFFFFDG"]
        testCaseSlimps = ["AH", "ABAHC", "ABABAHCC", "ADFGC", "ADFFFFGC", "ABAEFGCC", "ADFDFGC"]
        testCaseNotSlimps = ["ABC", "ABAH", "DFGC", "ABABAHC", "SLIMP", "ADGC"]
        testCaseSlurpys = ["AHDFG", "ADFGCDFFFFFG", "ABAEFGCCDFEFFFFFG"]
        testCaseNotSlurpys = ["AHDFGA", "DFGAH", "ABABCC"]
    putStrLn "-----------------------------------------------------"
    putStrLn $ "testCaseSlumps : " ++ show (all (test reSlump) testCaseSlumps) ++ " " ++ show testCaseSlumps
    putStrLn $ "testCaseNotSlumps : " ++ (show . not) (all (test reSlump) testCaseNotSlumps) ++ " " ++ show testCaseNotSlumps
    putStrLn $ "testCaseSlimps : " ++ show (all (test reSlimp) testCaseSlimps) ++ " " ++ show testCaseSlimps
    putStrLn $ "testCaseNotSlimps : " ++ (show . not) (all (test reSlimp) testCaseNotSlimps) ++ " " ++ show testCaseNotSlimps
    putStrLn $ "testCaseSlurpys : " ++ show (all testSlurpy testCaseSlurpys) ++ " " ++ show testCaseSlurpys
    putStrLn $ "testCaseNotSlurpys : " ++ (show . not) (all testSlurpy testCaseNotSlurpys) ++ " " ++ show testCaseNotSlurpys
    
    -- main program
    putStrLn "-----------------------------------------------------"
    putStr "input test count : "
    n <- getLine
    testCases <- forM [1..(read n::Int)] $ \i -> getLine
    -- result
    putStrLn "-----------------------------------------------------"
    putStrLn "SLURPYS OUTPUT"
    mapM_ putStrLn $ map (\testCase -> if (testSlurpy testCase) then "YES" else "NO") testCases
    putStrLn "END OF OUTPUT"
