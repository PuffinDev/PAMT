import sys
import os
import time
import json
import fnmatch
from progress.bar import Bar

# Python Anti-Malware Toolkit

root = "/"  #'/' for linux  'C:\' for windows
patterns = ['*.py', '*.sh']
matching_files = []
dangerous_files = []

bad_content = b'rm -rf' #Files that contain this text will be blacklisted

banner = \
'\u001b[34;1m' + """
-------------------------------
  _____        __  __ _______ 
 |  __ \ /\   |  \/  |__   __|
 | |__) /  \  | \  / |  | |   
 |  ___/ /\ \ | |\/| |  | |   
 | |  / ____ \| |  | |  | |   
 |_| /_/    \_\_|  |_|  |_|   

 Python Anti-Malware Toolkit
-------------------------------


""" + '\u001b[0m'

print(banner)


def scan():
    global files

    #scan filesystem

    filecount = 0
    print("Initialising...")
    for path, subdirs, files in os.walk(root):  #Count files for progress bar
        for name in files:
            filecount += 1
    print('\n')

    bar = Bar('Scanning filesystem', max=filecount)
    previous = ""
    for path, subdirs, files in os.walk(root):  #Find files with specified patterns
        for name in files:
            for pattern in patterns:
                if fnmatch.fnmatch(name, pattern):
                    matching_files.append(os.path.join(path, name))
            bar.next()
    print('\n')

    scan_files(matching_files)
    
    

def scan_files(files):
    #scan list of filenames
    bar2 = Bar('Identifying threats', max=len(files))

    for file in files:  #Scan files for a string
        try:
            with open(file, 'rb') as f:
                with open("database/lines.json", 'r') as f2:
                    database = json.load(f2) 

                    for bad_content in database.values():
                        bad_content = bad_content[0][0]
                        bad_content = bytes(bad_content, 'utf-8')
                        
                        if bytes(bad_content) in f.read():
                            dangerous_files.append([bad_content.decode('utf-8'), file])
        except FileNotFoundError:
            pass
        bar2.next()

    
    with open("output.txt", 'w+') as f:
        for file in dangerous_files:
            f.write(file[0] +  "  --> " + file[1] + '\n')

    print('\u001b[33m' + '\n\n' + str(len(dangerous_files)) + " Malicious files detected" + '\u001b[0m')
    print("See the full list of files in output.txt")

scan()