import os, glob, collections

f = open("README.md","w")

ignores = (".git", "__pycache__", ".ropeproject","src")

languages = collections.OrderedDict({
    "C" : "*.c",
    "C++" : "*.cpp",
    "Go" : "*.go",
    "Haskell" : "*.hs",
    "Julia" : "*.jl",
    "Python" : "*.py",
    })


totalResolve = collections.OrderedDict()
    
for lang in languages:
    totalResolve[lang] = 0

index = 1
listDir = list(os.listdir())
listDir.sort()
for folder in listDir:
    if os.path.isdir(folder) and folder not in ignores:
        print("*", index, folder, file=f)
        index += 1
        for lang in languages:
            files = list(glob.glob(os.path.join(folder, languages[lang])))
            numFiles = len(files)
            filenames = ", ".join([os.path.split(filename)[1] for filename in files])            
            print("\t* %s(%d) : %s" % (lang, numFiles, filenames), file=f)
            totalResolve[lang] += numFiles
        print("", file=f)
        
print("-"*40, file=f)
print("Total resolved info", file=f)
print("-"*40, file=f)
        
for lang in languages:
    print("\t%s : %d solved" % (lang, totalResolve[lang]), file=f)
    
f.close()

f = open("README.md","r")
print(f.read())
f.close()
