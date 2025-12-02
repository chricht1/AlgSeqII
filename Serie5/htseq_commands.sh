htseq-count -f bam -r pos -t exon -i gene_id -n 6 Data/Saccharomyces_RefGenome_R64/Bowtie/bowtie_map_sorted.bam Data/Saccharomyces_RefGenome_R64/NCBI_RefSeq_Assembly/genomic.gtf | tee Data/Saccharomyces_RefGenome_R64/Bowtie/htseq_nonunique_transcr_counts.tsv

htseq-count -f bam -r pos -t exon -i gene_id -n 6 Data/Saccharomyces_RefGenome_R64/Star/star_Aligned.sortedByCoord.out.bam Data/Saccharomyces_RefGenome_R64/NCBI_RefSeq_Assembly/genomic.gtf | tee Data/Saccharomyces_RefGenome_R64/Star/htseq_nonunique_transcr_counts.tsv
