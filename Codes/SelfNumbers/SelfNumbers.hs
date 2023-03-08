import Data.Char
import Data.List
generate n = n + sum [digitToInt x | x <- (show n)]
print $ sum $ [1..4999] \\ [generate x|x<-[1..4999]] 