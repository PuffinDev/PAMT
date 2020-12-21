import sys
import os
import time
import json
import fnmatch
from progress.bar import Bar

# Python Anti-Malware Toolkit

root = "/"
patterns = ['.py']
files = []

def scan():
    global files

    #scan filesystem

    filecount = 0

    for path, subdirs, files in os.walk(root):
        for name in files:
            filecount += 1

    print(filecount)

    bar = Bar('Scanning filesystem', max=filecount)

    for path, subdirs, files in os.walk(root):
        for name in files:
            #print("Scanning " + name)
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    files.append(os.path.join(path, name))
            bar.next()
    print('\n')
    
    bar = Bar('Identifying threats', max=len(files))

    for file in files:
        with open(file) as f:
            if 'import threading' in f.read():
                print("Malware detected in '" + file + "'")
    

def scan_file(file):
    #scan invividual file
    pass

scan()