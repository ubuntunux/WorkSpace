doCycle n xs
    | n < 0 = take lenXS $ drop (abs n) $ cycle xs
    | n > 0 = take lenXS $ drop (lenXS - mod (abs n) lenXS) $ cycle xs
    | otherwise = xs
    where
        lenXS = length xs

strCycle n xs = do
    putStrLn $ "Input : " ++ (show n) ++ " " ++ xs
    putStrLn $ "Output : " ++ (unwords $ doCycle n $ words xs) ++ "\n"

-- test function, Just Run
main = do
    strCycle 1 "10 20 30 40 50"
    strCycle 4 "가 나 다 라 마 바 사"
    strCycle (-2) "A B C D E F G"
    strCycle 0 "똘기 떵이 호치 새초미"
