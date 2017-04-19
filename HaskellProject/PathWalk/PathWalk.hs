module PathWalk
( pathWalk
, splitFileOrDir
, showDirectory
, test
) where

import System.Directory
import System.FilePath.Posix
import Control.Monad

type DirName = String
type FileName = String
data Directory = Directory DirName [FileName] [Directory] deriving (Show)

splitFileOrDir curDir [] = return ([],[])
splitFileOrDir curDir (x:xs) = do 
    isDir <- doesDirectoryExist (joinPath [curDir, x])
    (xp, yp) <- splitFileOrDir curDir xs
    if isDir 
        then return (x:xp, yp)
        else return (xp, x:yp)


pathWalk curDir = do
    contents <- getDirectoryContents curDir
    contents <- return [x | x <- contents, not (elem x [".", ".."]) ]    
    (dirs, files) <- splitFileOrDir curDir contents
    result <- forM dirs (\dir -> do
            pathWalk (joinPath [curDir, dir])
            )
    return $ Directory curDir files result

showDirectory (Directory dirName files dirs) = do
    putStrLn $ "Directory :" ++ dirName
    let numFiles = length files
    when (numFiles > 0) $ putStrLn $ "Files(" ++ (show numFiles) ++ ") :"
    mapM (\x->putStrLn ("\t" ++ x)) files
    forM dirs (\dir -> do
            putStrLn ""
            showDirectory dir
            )
    return ()


test dirPath = pathWalk dirPath >>= (showDirectory)

