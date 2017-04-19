splitEvenOdd [] = ([], [])
splitEvenOdd (x:xs)
    | mod x 2 == 0 = (x:xp, yp)
    | otherwise = (xp, x:yp)
    where (xp, yp) = splitEvenOdd xs
    

main = print $ splitEvenOdd [1..10]
