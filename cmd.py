import argparse
parser = argparse.ArgumentParser()
parser.add_argument("filePath", help="Path to the image")
args = parser.parse_args()

import recognizer

islavalamp = recognizer.recognize(args.filePath)

print(islavalamp)