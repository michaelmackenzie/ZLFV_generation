#!/bin/env python

import os
import subprocess
import sys
import argparse
import math

def list_of_files(path):
    if path[-1] != "/": path = path + "/"
    files= subprocess.check_output(["ls", path]).splitlines()
    outfiles=[]
    for line in files:
        if ".root" in line and "MERGE" not in line:
            outfiles.append(path + line)
    return outfiles

p = argparse.ArgumentParser(description='Submit MC generation jobs')

p.add_argument('--input'       , help='Input directory', required=True)
p.add_argument('--merge_factor', help='Input to output merging factor', type=int, required=True)
p.add_argument('--remove_after', help='Remove the input dataset after merging', default=False, action='store_true', required=False)

args = p.parse_args()

path   = args.input
factor = args.merge_factor
remove = args.remove_after
if remove:
    print "Removing input dataset after merging!"

files = list_of_files(path)
nfiles = len(files)
if nfiles == 0:
    print "No files found in path", path
    exit()

name = files[0].split("/")[-1]
name = name.replace(name.split("_")[-1], "")
name = "MERGE_" + name
print "Using base name", name

nstart = 0

for count in range(0, int(math.ceil(nfiles*1.0/factor))):
    nend = min(nfiles, nstart+factor)
    files_to_merge = files[nstart:nend]
    if len(files_to_merge) == 0: break
    out_name = "%s%s%i.root" % (path, name, count)
    command = "%s/src/ZLFV_generation/scripts/haddnano.py %s" % (os.environ['CMSSW_BASE'], out_name)
    for line in files_to_merge: command += " %s" % (line)
    print ">>> Merging subset %i" % (count)
    os.system(command)
    if remove:
        print ">>> Removing input dataset %i" % (count)
        for line in files_to_merge: os.system("rm %s" % (line))
    nstart += factor
