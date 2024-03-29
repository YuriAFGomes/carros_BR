import os
import sys
from pathlib import Path

dir = sys.argv[1]


files = [file for file in os.listdir(dir) if not os.path.isdir(os.path.join(dir,file))]
file = sorted(files,key=len)

try:
    os.mkdir('temp')
except:
    pass

temp = "temp"

for file in files:
    new_name = f"{files.index(file)+1}.jpg"
    os.rename(os.path.join(dir,file),os.path.join(temp,new_name))
    os.rename(os.path.join(temp,new_name),os.path.join(dir,new_name))
