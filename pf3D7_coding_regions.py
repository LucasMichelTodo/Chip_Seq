#!/usr/bin/env python

import pandas
import csv

# Import data.frame with exons
exons = pandas.DataFrame.from_csv(path = "/home/lucas/ISGlobal/Gen_Referencies/true_exons.txt", sep=" ", header=None, index_col=None)
exons.columns=["chrom", "type", "start", "stop"]
grouped_df = exons.groupby("chrom")

# Group by chrmosome and sort
df = exons.sort_values(by="start",axis=0).groupby("chrom")

# Creating a dictionary with chromosomes as keys and start-stop positions as a list of tuples
coding = {}
for name, group in df:
	for idx, row in group.iterrows():
		if name in coding:
			coding[name].append((row["start"], row["stop"]))
		else:
			coding[name] = [(row["start"], row["stop"])]


# Purging ovelapping exons (alternative splicing). 
n_iter = [1,2] #setting number of needed iterations
for i in n_iter:
	for key in coding:
		for i in range(len(coding[key])-1):
				if coding[key][i][1] > coding[key][i+1][0]:
					coding[key][i] = (min([coding[key][i],coding[key][i+1]])[0], max([coding[key][i],coding[key][i+1]])[1])
					coding[key][i+1] = (0,0) # Set the ones to remove to (0,0)
				else:
					pass

for key in coding:
	coding[key] = [i for i in coding[key] if i[0] > 0] # Remove all (0,0)


# Checking no more overlaps are present.
for key in coding:
	for i in range(len(coding[key])-1):
			if coding[key][i][1] > coding[key][i+1][0]:
				print "Ojut!"
				print coding[key][i]
				print coding[key][i+1]
			else:
				pass

# Create non coding dictionary

# First load chromosome sizes
sizes = {}
with open("/home/lucas/ISGlobal/Gen_Referencies/Pf3D7.sizes", "rb") as csvfile:
	chrom_sizes = csv.reader(csvfile, delimiter='\t')
	for row in chrom_sizes:
		if len(row) == 2:
			sizes[row[0]] = row[1]
		else:
			pass

sizes["Pf_M76611"] = sizes.pop("M76611")
sizes["Pf3D7_API_v3"] = sizes.pop("PFC10_API_IRAB")


# Then create noncoding dictionary
noncoding = {}

for key in coding:
	noncoding[key] = []
	for i in range(len(coding[key])):
		if i == 0:
			noncoding[key].append((1,coding[key][i][0]-1))
		else:
			noncoding[key].append((coding[key][i-1][1]+1, coding[key][i][0]-1))

for key in noncoding:
	noncoding[key].append((coding[key][-1][1]+1, sizes[key]))


# Eliminate those tuples that are "inverted" (generated by either position 1 in coding tuple or concecutive positions in coding tuple)

for key in noncoding:
	noncoding[key] = [i for i in noncoding[key] if i[0] < i[1]] # Remove all (i>i)
