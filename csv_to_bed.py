#!/usr/bin/env python

# Import packages 
import sys
import pandas as pd

def csv_to_bed(csv_file):

	bed = pd.read_csv(filepath_or_buffer= csv_file, sep="\t", header=None, index_col=None, skiprows=1, usecols=[1,2,3,4,5,6,7,8,9,10])

	bed.to_csv(path_or_buf=csv_file.replace(".csv", ".bed"), sep="\t", header=False, index=False)






if __name__ == "__main__":
	filenames = sys.argv[1:]
	print filenames
	for element in filenames:
		csv_to_bed(element)