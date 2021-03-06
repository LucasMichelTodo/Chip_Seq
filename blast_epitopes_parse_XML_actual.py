#!/usr/bin/env python

import sys
import subprocess
from Bio.Blast import NCBIXML

def parse_blastp(blast_xml):

    result_handle = open(blast_xml) #Run BLAST fom web interface first and download xml output (much faster)
    blast_records = NCBIXML.parse(result_handle)

    best_hits = []

    for record in blast_records:

        epitope_length = record.query.split(" | ")[1]
        #epitope_length = 9
        hits = []
        for alignment in record.alignments:
            for hsp in alignment.hsps:
                #print(hsp.query)
                #print alignment.title

                hits.append((alignment.title.split("|")[3], float(hsp.identities)/int(epitope_length)*100, hsp.expect, hsp.bits))
                #hits.append((alignment.title.split("|")[3], float(hsp.identities)/9*100, hsp.expect))
                sorted_hits = sorted(hits, key=lambda x: x[3], reverse=True)
                #print sorted_hits
                #print "++++++++++++++++++++++"

        try:
            best_hits.append((record.query[3:], sorted_hits[0]))
            sorted_hits = []
        except:
            best_hits.append((record.query[3:], ""))
            sorted_hits = []
            #print "hopla!", record.query

        #print "-------------------------------------"
        #print best_hits
        #print "-------------------------------------"

    with open("/media/lucas/Disc4T/Projects/tcruzi_Actual/Run_Exposed/B_predictions/blasted_microbiome.csv", "r+") as infile:
        for line in infile:
            epitope = line.strip().split("\t")[0]
            #print line.strip().split("\t")
            # print len(line.strip().split("\t"))

            if len(line.strip().split("\t")) == 3:

                for i in best_hits:
                    if i[0].split(" | ")[0] == epitope:
                        blast_result = [str(x) for x in i[1]]
                        print line.strip()+"\t"+"\t"+"\t"+"\t"+"\t".join(blast_result)

            # print line.strip().split("\t")
            # print len(line.strip().split("\t"))
            else:
                for i in best_hits:
                    if i[0].split(" | ")[0] == epitope:
                        blast_result = [str(x) for x in i[1]]
                        print line.strip()+"\t"+"\t".join(blast_result)



if __name__ == "__main__":
    filenames = sys.argv[1:]
    for i in filenames:
        parse_blastp(i)
