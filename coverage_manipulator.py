#!/usr/bin/env python

import pysam
import csv 
import sys
import numpy
import pandas as pd


#Numberof reads after filtering in treatment:
depths = {"10G":4535787.0, "1.2B":4997472.0, "A7": 10915415.0, "C2": 5176848.0, "E5": 9366386.0}

#Calculate coverage over whole genome:
def coverage(bamfile):

	sam = pysam.AlignmentFile(bamfile, "rb")

	chrom_cov = {}
	sizes = {}
	
	with open("/home/lucas/ISGlobal/Gen_Referencies/Pf3D7.sizes", "rb") as csvfile:
		chrom_sizes = csv.reader(csvfile, delimiter='\t')
		for row in chrom_sizes:
			if len(row) == 2:
				sizes[row[0]] = row[1]
			else:
				pass

	for key in sizes:
		coverage = []
		cov = sam.count_coverage(reference=key, start=1, end=int(sizes[key]))
		total_cov = numpy.sum(cov, axis=0)+1
		print "total_cov"
		print total_cov
		smooth_cov = numpy.array(pd.Series(total_cov).rolling(200, min_periods=1).mean().tolist())
		chrom_cov[key] = smooth_cov
		print "smooth_cov"
		print smooth_cov

	return chrom_cov

# "Normalize" coverage diving by reads after filtering and multiplying by 1000000:
def normalize_coverage(bamfile):
	
	norm_cov = {}
	abs_cov = coverage(bamfile)
	for key in depths:
		if key in bamfile:
			for chrom in abs_cov:
				norm_cov[chrom] = abs_cov[chrom]/depths[key]*1000000
				print "norm_cov"
				print norm_cov[chrom]
				 
	return norm_cov


# Substract two "normalized" coverage traks:
def susbstract_norm_cov(bam1, bam2):

	sub_cov = {}
	dict1 = normalize_coverage(bam1)
	dict2 = normalize_coverage(bam2)

	for key in dict1:
		sub_cov[key] = dict1[key] - dict2[key]

	for key in sub_cov:
		i = 0
		for element in sub_cov[key]:
			with open("result_2.txt", "a+") as bed_file:
				bed_file.write("{}\t{}\t{}\t{}\n" .format(key, i, i+1, element))
				i += 1

	return sub_cov


def ratio_norm_cov(bam1, bam2):
	
	ratio_cov = {}
	dict1 = normalize_coverage(bam1)
	dict2 = normalize_coverage(bam2)

	for key in dict1:
		ratio_cov[key] = numpy.log(dict1[key] / dict2[key])

	for key in ratio_cov:
		i = 0
		for element in ratio_cov[key]:
			with open(bam1+"_RATIO5_"+bam2+".txt", "a+") as bed_file:
				bed_file.write("{}\t{}\t{}\t{}\n" .format(key, i, i+1, element))
				i += 1

	return ratio_cov



def compare_to_input(treat, control):

	input_cov = {}
	treat_cov = normalize_coverage(treat)
	treat_cov_pseudo = {}
	for key in treat_cov:
		treat_cov_pseudo[key] = treat_cov[key]+1

	control_cov = normalize_coverage(control)
	control_cov_pseudo = {}
	for key in control_cov:
		control_cov_pseudo[key] = control_cov[key]+1

	for key in treat_cov_pseudo:
		input_cov[key] = numpy.log2((treat_cov_pseudo[key]/control_cov_pseudo[key]))

	for key in input_cov:
		i = 0
		for element in input_cov[key]:
			with open("normalized_by_depthandinput.bed", "a+") as bed_file:
				bed_file.write("{}\t{}\t{}\t{}\n" .format(key, i, i+1, element))
				i += 1

	return input_cov


def print_coverage_at_intervals(bamfile, inter):

	dict1 = normalize_coverage(bamfile)
	
	for key in dict1:
		pos = 0
		i = 0
		cov = 0

		for element in dict1[key]:
			cov += element
			i += 1
			pos += 1

			if i == int(inter):

				with open(bamfile.replace(".bam", "_fullcoverage.bed"), "a+") as bed_file:
					print bamfile.replace(".bam", "_fullcoverage.bed")
					bed_file.write("{}\t{}\t{}\t{}\n" .format(key, pos-i, pos, cov))
					i = 0
					cov = 0
					pos = pos+i

###### Change this part to use whatever function you like.

if __name__ == "__main__":
	filenames = sys.argv[1:]
	print_coverage_at_intervals(filenames[0], filenames[1])