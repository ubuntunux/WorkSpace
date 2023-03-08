import os, sys

failed = []

def convertEncoding(filename, newEncoding='UTF-8'):
    print("Try to convertEncoding :", filename)
    for encoding in ('UTF-8', 'Shift-JIS', 'euc-kr'):
        try:
            # read file
            f = open(filename, "r", encoding=encoding)
            body = f.read()
            f.close()
            # pass if file is correct encoding
            if encoding == newEncoding:
                return
            # convert encoding
            f = open(filename, 'w', encoding=newEncoding)
            f.write(body)
            f.close()
            return
        except:
            pass
    else:
        global failed
        failed.append(filename)
        

def main(workDir='.'):
    for dirname, dirnames, filenames in os.walk(workDir):
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() in ('.fx', '.cpp', '.h', '.rc'):
                convertEncoding(os.path.join(dirname, filename))
    # show failed encoding list
    if failed:
        for fail in failed:
            print("\t- Encoding failed.", fail)
        print("%d Error(s)" % len(failed))
    else:
        print("All Success.")
	
    
# run
if __name__ == '__main__':
    main(sys.argv[1])