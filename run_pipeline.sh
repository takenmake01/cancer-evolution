#!/usr/bin/bash

# get sequences and generate .fasta files with python
python ./pull_seq.py

# run tcoffee to generate .aln alignment files
# NOTE: program is expecing the tcoffee github to be cloned in the same directory cancer-evolution was cloned to
# tcoffee github (follow manual compile instructions in the readme): https://github.com/cbcrg/tcoffee/tree/master
MAX_N_PID_4_TCOFFEE=1000000 ../tcoffee/binaries/linux/t_coffee fastaFiles/sequenceList_cd28_g.fasta -multi_core=msa -thread=0 -outfile=alignments/cd28_g.aln
MAX_N_PID_4_TCOFFEE=1000000 ../tcoffee/binaries/linux/t_coffee fastaFiles/sequenceList_ctla4_g.fasta -multi_core=msa -thread=0 -outfile=alignments/ctla4_g.aln
MAX_N_PID_4_TCOFFEE=1000000 ../tcoffee/binaries/linux/t_coffee fastaFiles/sequenceList_icos_g.fasta -multi_core=msa -thread=0 -outfile=alignments/icos_g.aln
MAX_N_PID_4_TCOFFEE=1000000 ../tcoffee/binaries/linux/t_coffee fastaFiles/sequenceList_pd1_g.fasta -multi_core=msa -thread=0 -outfile=alignments/pd1_g.aln
MAX_N_PID_4_TCOFFEE=1000000 ../tcoffee/binaries/linux/t_coffee fastaFiles/sequenceList_cd28_p.fasta -multi_core=msa -thread=0 -outfile=alignments/cd28_p.aln
MAX_N_PID_4_TCOFFEE=1000000 ../tcoffee/binaries/linux/t_coffee fastaFiles/sequenceList_ctla4_p.fasta -multi_core=msa -thread=0 -outfile=alignments/ctla4_p.aln
MAX_N_PID_4_TCOFFEE=1000000 ../tcoffee/binaries/linux/t_coffee fastaFiles/sequenceList_icos_p.fasta -multi_core=msa -thread=0 -outfile=alignments/icos_p.aln
MAX_N_PID_4_TCOFFEE=1000000 ../tcoffee/binaries/linux/t_coffee fastaFiles/sequenceList_pd1_p.fasta -multi_core=msa -thread=0 -outfile=alignments/pd1_p.aln

# generate phylogenetic trees
python ./phylo_tree_gen.py