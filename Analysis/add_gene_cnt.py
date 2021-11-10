import pyensembl
import pandas as pd
import sys

ensembl=pyensembl.EnsemblRelease(release=102)
fl=sys.argv[1]
df=pd.read_csv(fl,sep='\t')
dic={}

for line in range(len(df)):
	chrom, pos = df.loc[line,"#CHROM"],df.loc[line,"POS"]
	chrom = chrom.replace("chr","")
	if chrom.isdigit():
		chrom = int(chrom)
	gene_names = ensembl.gene_names_at_locus(contig=chrom, position=int(pos))
	if not str(gene_names) in dic:
		dic[str(gene_names)] = 1
	else:
		dic[str(gene_names)]+=1

for line in range(len(df)):
	chrom, pos = df.loc[line,"#CHROM"],df.loc[line,"POS"]
	chrom = chrom.replace("chr","")
	if chrom.isdigit():
		chrom = int(chrom)
	gene_names = ensembl.gene_names_at_locus(contig=chrom, position=int(pos))
	df.loc[line,"Gene names"]=str(gene_names).replace("[","").replace("]","").replace("'",'')
	df.loc[line,"Gene count"]=dic[str(gene_names)]
df.to_excel("OV-SMC_gene_namecnt_3OVER.xlsx",index=0)
df2=df.drop_duplicates(subset=['Gene names','Gene count'])
#df2.to_excel("OV-SMC_gene_namecnt_dedup_4OVER.xlsx",index=0)

