import Data.Char (digitToInt)
import Control.Monad (join)

is_happy_number n history
    | sumnum == 1 = True
    | sumnum `elem` history = False
    | otherwise = is_happy_number sumnum (sumnum:history)
    where sumnum = sum [(digitToInt x)^2 | x<-show(n)]

test_happy_number n = join [show(n), " is ", (if is_happy_number n [] then "a Happy" else "an Unhappy"), " number."]

main = do
    mapM_ putStrLn $ map test_happy_number [3,7,4,13]
