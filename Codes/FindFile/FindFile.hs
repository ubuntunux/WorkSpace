import System.Directory
import System.FilePath.Posix
import Control.Monad
import Data.List

-- check isInfixOf "LIFE IS TOO SHORT"
isInfixOfText filename = do
    contents <- readFile filename
    if isInfixOf "LIFE IS TOO SHORT" contents
        then print filename
        else return ()
        
-- recursive search file function
searchDir curDir = do
    contents <- getDirectoryContents curDir
    forM_ [x | x <- contents, not (elem x [".", ".."])] (\content -> do
        let curContent = joinPath [curDir, content]
        isDir <- doesDirectoryExist curContent
        if isDir
            then searchDir curContent
            else isInfixOfText curContent
        )

-- run from current directory
main = searchDir "."

