bowtie-build --threads 4 \
-f Data/Saccharomyces_RefGenome_R64/NCBI_RefSeq_Assembly/GCF_000146045.2_R64_genomic.fna \
Data/Saccharomyces_RefGenome_R64/Bowtie/NCBI_RefSeq_Assembly_Bowtie_Idx/bowtie_idx

bowtie --best -S -p 4 --chunkmbs 200 --threads 4 \
-x Data/Saccharomyces_RefGenome_R64/Bowtie/NCBI_RefSeq_Assembly_Idx/bowtie_idx \
Data/SRR1258470/SRR1258470_trimmed.fastq > Data/Saccharomyces_RefGenome_R64/Bowtie/bowtie_out.sam

# reads processed: 13800105
# reads with at least one alignment: 12714872 (92.14%)
# reads that failed to align: 1085233 (7.86%)
# Reported 12714872 alignments


#samtools view -b bowtie_out.sam > bowtie_out.bam
samtools sort bowtie_out.sam -o bowtie_out_sorted.bam
samtools index bowtie_out_sorted.bam
