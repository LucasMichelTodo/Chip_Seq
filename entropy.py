#!/usr/bin/env python

from Bio.Align import AlignInfo
from Bio.Align.AlignInfo import SummaryInfo
from Bio import AlignIO
import sys
import pandas as pd
import scipy as sc
import scipy.stats

# Input a pandas series
def ent(data):
    p_data= data.value_counts()/len(data) # calculates the probabilities
    entropy=scipy.stats.entropy(p_data)  # input probabilities to get the entropy
    return entropy


def most_common(lst):
    return max(set(lst), key=lst.count)

# Function for calculating lenvenstein distance between two strings
def lv_number(a, b):
    string1 = a
    string2 = b
    distance = 0
    n1 = len(string1)
    n2 = len(string2)

    if n1 >= n2:
        for i in range(n1):
            if i < n2:
                if string1[i] != string2[i]:
                    distance += 1
            else:
                distance += 1
    else:
        for i in range(n2):
            if i < n1:
                if string2[i] != string1[i]:
                    distance -= 1
            else:
                distance -= 1


    return distance


# Input a ClustalW .aln file
def ClustalEnt(clustal_file):
    aa_var = [] # container for list of aa in a position
    entropies = [] # container for final entropy result per position
    consensus = [] # container for consenses sequence
    alignment = AlignIO.read(open(clustal_file), "clustal")

    #summary = SummaryInfo(alignment)
    #print summary.gap_consensus(threshold=0.4,ambiguous="*")[43]

    for i in range(0,alignment.get_alignment_length()):
        for record in alignment:
            aa_var.append(record.seq[i])
        data = pd.Series(aa_var)
        entropies.append(ent(data))

        #print aa_var
        #print most_common(aa_var)
        #print entropies[i]

        # Set entropy threshold:
        if ent(data) <= 9999:
            consensus.append(most_common(aa_var))

        else:
            consensus.append("*")

        aa_var = []

    consensus_str = "".join(consensus)

    current_min = 99999999999999999999999999999999999
    current_seq = ""
    current_ref = ""
    #ref_order = {'TcCLB':5, 'AODP0':4, 'AYLP0':7, 'AQHO0':2, 'TcChr':8, 'Tcruz':6, 'ANOX0':1, 'TcX10':3, 'Expos':0, 'TcMAR':9}
    ref_order = {'Tb11.':6, 'TcIL3':1, 'TvY48':2, 'TY486':2.1, 'Tb927':4, 'TevST':3, 'Tb427':5, 'Tb05.':7, 'Tb09.':8, 'Tb10.':9, 'Tb07.':10, 'Tb06.':11, 'Tb04.':12, 'Tb08.':13, 'N19B2':14, '13J3.':15, '13J1.':16, 'H25N7':17}

    for record in alignment:
        #print record.seq
        #print consensus_str
        #print lv_number(str(record.seq), consensus_str)
        if lv_number(str(record.seq), consensus_str) < current_min:
            #print "min!"
            current_min = lv_number(str(record.seq), consensus_str)
            current_seq = record.seq
            current_ref = record.id
        elif lv_number(str(record.seq), consensus_str) == current_min:
            if ref_order[record.id[0:5]] < ref_order[current_ref[0:5]]:
                #print "min!"
                #print "Current ref: {} ---> {}" .format(current_ref[0:5], ref_order[current_ref[0:5]])
                #print "New ref: {}---> {}" .format(record.id[0:5], ref_order[record.id[0:5]])
                current_min = lv_number(str(record.seq), consensus_str)
                current_seq = record.seq
                current_ref = record.id

    #print "\n"+current_seq

    ref = list(current_seq)
    masked_ref = ["*"] * len(ref)
    for i in range(0,len(ref)):
        if ref[i] == consensus[i]:
            masked_ref[i] = ref[i]

    ## Print result to screen
    #print "".join(masked_ref)

    ## Write result to _consensus file:
    # Creating header for consensus file. Setting "w+" ensures the file will be created from scratch if re-run.
    with open(clustal_file.replace("_sorted.aln", "_consensus_unmasked.fasta"), "w+") as file:
        file.write(">"+current_ref+"\n")
    with open(clustal_file.replace("_sorted.aln", "_consensus_unmasked.fasta"), "a+") as file:
        file.write("".join(masked_ref))




    #print entropies



if __name__ == "__main__":
    filenames= sys.argv[1:]
    print filenames
    for file in filenames:
        ClustalEnt(file)
