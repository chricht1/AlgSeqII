#!/bin/bash
input=../../Data/SRR1258470/SRR1258470.fastq.gz
output=SRR1258470_trimmed.fastq.gz
trimmomatic SE -phred33 $input $output HEADCROP:10 TAILCROP:10 LEADING:28 TRAILING:28 MINLEN:20