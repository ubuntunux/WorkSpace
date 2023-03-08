import Data.List

getTokens xs n = [take n (drop i xs) | i <- [0..(length xs - n)]]

findCommonString s1 s2 = if length result > 0 then head result else ""
    where
        (shortStr, longStr) = if length s1 < length s2 then (s1, s2) else (s2, s1)
        shortLength = length shortStr
        result = [token | n <- reverse [1..shortLength], token <- getTokens shortStr n, isInfixOf token longStr]

-- let's find common string.     
main = return $ findCommonString "photography" "autograph"
