import sys

if len(sys.argv) < 2:
    print(f"Missing image name")
    quit()

from recognizer import *

filePath = sys.argv[1]

islavalamp = recognize(filePath)

print(islavalamp)