#!/bin/bash

# achtung command ist für trimmomatic v0.40
# für trimmomatic v0.32 muss statt TAILCROP:10 CROP:81 gesetzt werden

input=../../Data/SRR1258470/SRR1258470.fastq.gz
output=SRR1258470_trimmed.fastq.gz
trimmomatic SE -phred33 -trimlog SRR1248470_trimlog.log $input $output HEADCROP:10 TAILCROP:10 LEADING:28 TRAILING:28 MINLEN:20
