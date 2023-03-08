import Data.Char (digitToInt)

material = ["   ", " - ", "|  ", "| |", "  |"]
numToDigit = [[1, 3, 0, 3, 1], [0, 4, 0, 4, 0], [1, 4, 1, 2, 1], [1, 4, 1, 4, 1], [0, 4, 1, 4, 0], [1, 2, 1, 4, 1], [1, 2, 1, 3, 1], [1, 4, 0, 4, 0], [1, 3, 1, 3, 1], [1, 3, 1, 4, 0]]

chain xs with n
    | n == 0 = []
    | otherwise = xs ++ with ++ (chain xs with (n-1))

showDigit size num = [chain (getLine i) "\n" (if i `mod` 2 == 0 then 1 else size) | i <- [0..4]]
    where
        digitNums = [digitToInt n |  n <- show num]
        getMaterial digitNum i = (numToDigit !! digitNum) !! i
        getLine i = foldl (\acc x -> acc ++ (head x:"") ++ (chain (x !! 1:"") "" size) ++ (last x:"") ++ " ") "" [material !! (getMaterial curDigitNum i) | curDigitNum <- digitNums]

-- Run
main = do mapM_ (\xs -> mapM_ putStr xs) [showDigit 2 12345, showDigit 3 67890, showDigit 0 0]