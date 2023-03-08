import Data.List
import Control.Monad

data1 = "<     >"

data2 =
    "########\n\
    \#<     #\n\
    \#  ##  #\n\
    \#  ##  #\n\
    \#     >#\n\
    \########"

data3 =
    "#######\n\
    \#<    #\n\
    \##### #\n\
    \#     #\n\
    \# #####\n\
    \# #   #\n\
    \# # # #\n\
    \#   #>#\n\
    \#######"

data4 = "<   #   >"

data5 =
    "########\n\
    \#<     #\n\
    \#     ##\n\
    \#    #>#\n\
    \########"

data6 =
    "#< #  #\n\
    \#  #  #\n\
    \#  # >#"

checkPatterns = [(0, -1), (-1, 0), (1, 0), (0, 1)]

findStartPoint datas num
    | index /= Nothing = Just (n, num)
    | length datas <= num = Nothing
    | otherwise = findStartPoint datas (num + 1)
    where
        index = elemIndex '<' (datas !! num)
        Just n = index

mergeNode [] = Nothing
mergeNode (x:xs) 
    | x == Nothing = mergeNode xs
    | otherwise = x
    
findEndPoint datas (x,y) checkedList =
    mergeNode (
        fmap
            (\(pX, pY) -> 
                let
                    (nX, nY) = (x+pX, y+pY)
                    character = (datas !! nY) !! nX
                in
                    if nY >=0 && nY < length datas && nX >= 0 && nX < length (datas !! nY) && not (elem (nX, nY) checkedList)
                    then case character of
                        '>' -> Just (nX, nY)
                        ' ' -> findEndPoint datas (nX, nY) ((x,y):checkedList)
                        otherwise -> Nothing
                    else Nothing)
            checkPatterns
        )

checkTheMaze =
    fmap
        (\mazeData -> do
            let maze = lines mazeData
            startPoint <- findStartPoint maze 0
            findEndPoint maze startPoint [])
        [data1, data2, data3, data4, data5, data6]
