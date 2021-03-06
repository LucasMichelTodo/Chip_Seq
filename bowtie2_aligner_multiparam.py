#!/usr/bin/env python

import sys
import os
import subprocess
from tqdm import tqdm
import re

## USAGE
## 1.- Create a directory and place there all "fastq" files for the alignment.
## 2.- Edit <inpath> and <outpath>. <inpath> must match the created directory.
## 3.- Edit <params>. <params> is a dictionary. Each entry defines a set of parameters for bowtie2.
## 4.- Run. For each entry in <params> a directory will be created and alignments produced using those parameters will be stored there.

# Set in/out paths
inpath = "/home/lucas/ISGlobal/TestSet/align_tests2/clean/clean_inputs/" 
outpath = "/home/lucas/ISGlobal/TestSet/align_tests2/clean/Prova/"

# Set params
params = {"params_1":"-p 4 --very-sensitive --local -5 4 -3 4 -I 50 -X 200", 
		"params_2":"-p 4 --very-sensitive --local -5 4 -3 4 -I 50 -X 10000",
		"params_3":"-p 4 --very-sensitive --local -5 12 -3 4 -I 50 -X 10000",
		"params_4":"-p 4 --very-sensitive --local -N 1 -5 12 -3 4 -I 50 -X 10000"}

# Run
fd_rawlist = os.listdir(inpath)
# regex = re.compile(r'.*li.*\.fastq$')
# fd_rawlist = filter(regex.search, fd_rawlist)

for key in params:
	subprocess.call("mkdir {}{}" .format(outpath, key), shell=True)
	names = []
	for file in fd_rawlist:
		names.append(file[0:4])

	for x in tqdm(names):
		cmd = "~/Programs/bowtie2-2.3.0-legacy/bowtie2 {} -x ~/Programs/bowtie2-2.3.0-legacy/Pf3D7 -1 {} -2 {} > {}"\
		 .format(params[key], inpath+x+"_read1_clean.fastq", inpath+x+"_read2_clean.fastq", outpath+key+"/"+x+".sam")
		subprocess.call(cmd, shell=True)





