import pyensembl

esb=pyensembl.EnsemblRelease(release=102)
#a = ensembl.gene_names_at_locus(contig=11, position=1189615)
#a = esb.transcript_ids_of_gene_name("TP53")
b="ENST00000680850"
#a = esb.transcript_sequence(b.split(".")[0])
a = esb.transcript_sequence(b)
print(a)
#for i in a:
#	gene_names2 = esb.transcript_sequence(i)
#	print(len(gene_names2))
