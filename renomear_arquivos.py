import os
import sys
from pathlib import Path

dir = sys.argv[1]


files = [file for file in os.listdir(dir) if not os.path.isdir(os.path.join(dir,file))]

try:
    os.mkdir('temp')
except:
    pass
temp = "temp"

for file in files:
    new_name = f"000{files.index(file)+1}.jpg"[-8:]
    os.rename(os.path.join(dir,file),os.path.join(temp,new_name))

# files = [file for file in os.listdir(dir) if not os.path.isdir(os.path.join(dir,file))]
#
# for file in files:
#     os.rename(os.path.join(dir,file),os.path.join(dir,file.replace('_','')))
