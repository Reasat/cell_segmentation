import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--root')
args = parser.parse_args()
# Set the directory you want to start from
rootDir = args.root
for dirName, subdirList, fileList in os.walk(rootDir):
    print('Found directory: %s' % dirName)
    for fname in fileList:
       print('\t%s' % fname)