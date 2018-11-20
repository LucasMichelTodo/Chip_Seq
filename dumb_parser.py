#!/usr/bin/env python

import sys

def parse_consensus(consensus_file):

    refs = []
    with open("/home/lucas/ISGlobal/Cruzi/tcruzi_epitopes_vaccine/kmp11_epitope_blast_hits.txt", "r+") as ref:
        for line in ref:
            refs.append(line.strip())

        refs = [x.split(" | ")[2] for x in refs]

    fasta = {}
    seq = ""
    prot = ""

    with open(consensus_file, "r+") as file1:
        for line in file1:
            if line.startswith(">"):
                fasta[prot] = seq
                seq = ""
                prot = line.strip()
            else:
                seq += line.strip()

        fasta[prot] = seq

    for prot, seq in fasta.iteritems():
        if prot:
            if prot.startswith(">exposed"):
                pass
            else:
                loc = prot.split(" | ")
                loc = [x for x in loc if x.startswith('location=')][0]

                if loc in refs:
                    print prot
                    print seq

    # with open(consensus_file, "r+") as infile:
    #     for line in infile:

            # linelist = line.strip().split("\t")
            # #print linelist
            # print (">"+linelist[0]+" | "+linelist[2]+" | "+linelist[3]+"\n"+linelist[1])





#def parse_consensus(filein):

    # i = 1
    # ref = []
    # with open("/home/lucas/ISGlobal/Brucei/aat_vaccine/Run_060818/all_consensus00_onlyAA_15aa.fasta", "r+") as infile1:
    #     for line in infile1:
    #         if line.startswith(">"):
    #             #print i, "_".join(line.split("_")[0:3])
    #             ref.append(line.split(".")[0].strip())
    #             i +=1
                #print ref
#
#
    # with open(filein, "r+") as infile:
    #     i = 1
    #     for line in infile:
    #         ag = line.strip().split()[1]
    #         seq = line.strip().split()[0]
    #         fasta_header = ">Epitope_{} | {} | {}" .format(i,ag,len(seq))
    #         with open("/home/lucas/ISGlobal/Cruzi/tcruzi_epitopes_vaccine/Microbiome/New_run_091018/Fastas/{}.fasta" .format(seq), "w+") as fileout:
    #             fileout.write(fasta_header+"\n"+seq)
    #         i += 1


            # if line.startswith(">"):
            #     prot = line.strip().split(" | ")[0].strip()
            #     print prot
            #     if prot in ref:
            #         print line.strip()
            #
            # else:
            #     if prot in ref:
            #         print line.replace("-", "").replace("*","X").strip()


            # if line.strip() not in ref:
            #     print line

if __name__ == "__main__":
    filename= sys.argv[1]
    # parse_consensus(filename)
    parse_consensus(filename)