#!/bin/bash

# create index
STAR --runThreadN 4 \
--runMode genomeGenerate \
--genomeDir Data/Saccharomyces_Genome_R64/Star/Star_Genome_Idx \
--genomeFastaFiles Data/Saccharomyces_Genome_R64/NCBI_RefSeq_Assembly/GCF_000146045.2_R64_genomic.fna \
--sjdbGTFfile Data/Saccharomyces_Genome_R64/NCBI_RefSeq_Assembly/genomic.gtf \
--sjdbOverhang 80

# mapping:
STAR --runThreadN 4 \
--genomeDir Data/Saccharomyces_Genome_R64/Star/Star_Genome_Idx \
--readFilesIn Data/SRR1258470/SRR1258470_trimmed.fastq \
--outSAMtype BAM SortedByCoordinate \
--outFileNamePrefix Data/Saccharomyces_Genome_R64/Star/star_map_sorted_

