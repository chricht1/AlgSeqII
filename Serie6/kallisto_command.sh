kallisto index -t 4 -i Data/Saccharomyces_RefGenome_R64/NCBI_RefSeq_Assembly/kallisto_SRX_trimmed.idx Data/Saccharomyces_RefGenome_R64/NCBI_RefSeq_Assembly/transcripts_gffread.fa

[build] loading fasta file Data/Saccharomyces_RefGenome_R64/NCBI_RefSeq_Assembly/transcripts_gffread.fa
[build] k-mer length: 31
KmerStream::KmerStream(): Start computing k-mer cardinality estimations (1/2)
KmerStream::KmerStream(): Start computing k-mer cardinality estimations (1/2)
KmerStream::KmerStream(): Finished
CompactedDBG::build(): Estimated number of k-mers occurring at least once: 8256548
CompactedDBG::build(): Estimated number of minimizer occurring at least once: 2065785
CompactedDBG::filter(): Processed 8752210 k-mers in 6478 reads
CompactedDBG::filter(): Found 8240513 unique k-mers
CompactedDBG::filter(): Number of blocks in Bloom filter is 56443
CompactedDBG::construct(): Extract approximate unitigs (1/2)
CompactedDBG::construct(): Extract approximate unitigs (2/2)
CompactedDBG::construct(): Closed all input files

CompactedDBG::construct(): Splitting unitigs (1/2)

CompactedDBG::construct(): Splitting unitigs (2/2)
CompactedDBG::construct(): Before split: 15085 unitigs
CompactedDBG::construct(): After split (1/1): 15085 unitigs
CompactedDBG::construct(): Unitigs split: 174
CompactedDBG::construct(): Unitigs deleted: 0

CompactedDBG::construct(): Joining unitigs
CompactedDBG::construct(): After join: 11295 unitigs
CompactedDBG::construct(): Joined 3790 unitigs
[build] building MPHF
[build] creating equivalence classes ... 
[build] target de Bruijn graph has k-mer length 31 and minimizer length 23
[build] target de Bruijn graph has 11295 contigs and contains 8247587 k-mers 



kallisto quant --single -l 200 -s 80 -o Data/Kallisto/ -i Data/Saccharomyces_RefGenome_R64/NCBI_RefSeq_Assembly/kallisto_transcripts_gffread.idx Data/SRR1258470/SRR1258470_trimmed.fastq


#kallisto vs bowtie:
# es gibt jeweils transkripte die beim einen Abundanzen von 0 haben und höhere Abundanzen beim anderen
# aber größtenteils gemeinsamer Konsens
# liegt an untersch. Vorgehensweise 

#kallisto vs star:
# ähnlich wie kallisto vs bowtie
# hisat sehr ähnlich
# star mit multimapping (reads können an mehreren genen mappen)


#star vs bowtie aus Serie 5:
# ähnlicher zueinander als mit 
# splice awareness von star könnte grund sein wenn kein multimapping

# im igv im detail anschauen