import argparse
parser = argparse.ArgumentParser()
parser.add_argument("filePath", help="Path to the image")
args = parser.parse_args()

from recognizer import *

islavalamp = recognize(args.filePath)

print(islavalamp)