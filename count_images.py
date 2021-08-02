from PIL import Image  
import os
from os import walk
import matplotlib.pyplot
cwd = os.getcwd()

ind = 0
base = 'Image-'
for r, d, f in os.walk(cwd):
    for file in f:
        filename = base + str(ind)
        if(file.split(".")[1] != "py"):
            os.rename(file, filename + ".png")
        ind = ind + 1