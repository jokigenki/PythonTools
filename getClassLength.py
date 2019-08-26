
# This script will check all files in the given folder,
# and output the number of files, the total file size
# and any files above a specified line length (default 500)
# Specify 
# Usage: python(3) GetClassLength.py 

import os
import argparse

# internal class used to store class file data
class ClassInfo:
    def __init__(self, ext):
        self.ext = ext
        self.count = 0
        self.size = 0
        self.longFiles = dict()
    
    def countLines(self, path):
        c = 0
        try:
            c = sum(1 for line in open(path))
        except:
            c = 0
        return c

    def addFile (self, path):
        self.count += 1
        self.size += os.stat(path).st_size
        count = self.countLines(path)
        if count > args.limit:
            shortPath = path.split(args.source)[1]
            self.longFiles[shortPath] = count
    
    def getLongFiles (self):
        if len(self.longFiles) == 0:
            return f'There are no long {self.ext} files'
        lStr = '\n'.join(['%s: - %s' % kv for kv in self.longFiles.items()])
        return f'There are {len(self.longFiles)} long ({args.limit}+ line) {self.ext} files:\n' + lStr

    def getSizeStr (self):
        v = self.size
        v /= 1024
        if v < 1024:
            return f'{self.ext} size is {v:.1f}KB'
        v /= 1024
        if v < 1024:
            return f'{self.ext} size is {v:.1f}MB'
        v /= 1024
        return f'{self.ext} size is {v:.1f}GB'

parser = argparse.ArgumentParser(description='Get the class length of Obj-c(.h/.m) and Swift classes in the given folder.')
parser.add_argument('source', help='The source folder to scan.')
parser.add_argument('--log', help='Output to a log file.')
parser.add_argument('--limit', type=int, help='Any files longer than this will be printed to the console.', default='500')
args = parser.parse_args()

def printAndLog (value):
    print(value)
    if args.log != None and args.log != '':
        with open(args.log, 'a+') as f:
            f.write(value + "\n")

if args.log != None and os.path.isdir(args.log):
    print (f'Log must be a file, not a folder')
    exit()

if os.path.exists(args.log):
    overwrite = input('log exists, overwrite(o), append(a) or cancel(c)?')
    if overwrite == 'o':
        open(args.log, 'w').close()
    elif overwrite == 'c':
        exit()

printAndLog(f'--------------------------------------------------------------------------------')
printAndLog(f'Checking {args.source}')

hClassInfo = ClassInfo('.h')
mClassInfo = ClassInfo('.m')
swiftClassInfo = ClassInfo('.swift')

classInfo = [hClassInfo, mClassInfo, swiftClassInfo]
for root, dirs, files in os.walk(args.source):
    for f in files:
        path = os.path.join(root, f)
        ext = os.path.splitext(f)[1]
        for ci in classInfo:
            if ext == ci.ext:
                ci.addFile(path)

objcSize = (hClassInfo.size + mClassInfo.size) / 1024
swiftSize = swiftClassInfo.size / 1024

printAndLog(f'There are {hClassInfo.count} .h files, {mClassInfo.count} .m files and {swiftClassInfo.count} swift files.')
for ci in classInfo:
    printAndLog('\n------------------------------------')
    printAndLog (ci.getSizeStr())
    printAndLog (ci.getLongFiles())
printAndLog('\n')

if args.log != None and args.log != '':
    print(f'wrote to log file at {args.log}')