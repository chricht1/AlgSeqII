#!/bin/bash
<<<<<<< HEAD
input=../../Data/SRR1258470/SRR1258470.fastq
output=SRR1258470_trimmed.fastq
# achtung command ist für trimmomatic v0.40
# für trimmomatic v0.32 muss statt TAILCROP:10 CROP:81 gesetzt werden
trimmomatic SE -phred33 $input $output HEADCROP:10 TAILCROP:10 LEADING:28 TRAILING:28 MINLEN:20
=======
input=../../Data/SRR1258470/SRR1258470.fastq.gz
output=SRR1258470_trimmed.fastq.gz
trimmomatic SE -phred33 -trimlog SRR1248470_trimlog.log $input $output HEADCROP:10 TAILCROP:10 LEADING:28 TRAILING:28 MINLEN:20
>>>>>>> 7cfed3599794a8c86b59ed21cb3e17e01f1e9a2a
