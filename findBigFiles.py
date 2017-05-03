import os
import sys

TO_MB = 1024*1024
try:
    path = sys.argv[1]
    msize = long(sys.argv[2])*TO_MB
except:
    print "usage: python __.py root_dir greater_than_size (in MBs)"
    sys.exit()

for root, dirs, files in os.walk(path):
    for file in files:
        full_path = root+os.sep+file
        if os.path.isfile(full_path):
            size = os.path.getsize(full_path)
            if size > msize:
                print full_path, size/(TO_MB)
