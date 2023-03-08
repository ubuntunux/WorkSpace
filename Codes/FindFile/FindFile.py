import os
import glob

def findFile(dirname = "."):
    for filename in glob.glob(os.path.join(dirname, "**/*.txt"), recursive=True):
        for encoding in ("UTF-8", "UTF-16", "euc-kr", "ascii"):
            try:
                with open(filename, "r", encoding=encoding) as f:
                    lines = f.read()
                    if 'LIFE IS TOO SHORT' in lines:
                        print(filename)
                    break
            except:
                pass

# Test
findFile("..")
