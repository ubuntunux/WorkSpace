import Data.List
s = [1, 3, 4, 8, 13, 17, 20]
main = print $ sortBy (\(x1, y1) (x2, y2) -> if abs(x1-y1) > abs(x2-y2) then GT else LT) (zip (init s) (tail s)) !! 0