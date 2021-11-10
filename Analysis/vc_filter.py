import pandas as pd

df=pd.read_excel("OV-SMC_TopMT_VCFQ_vcf.xlsx")
df1=df.loc[df["Total_TF"] >2]
df2=df1.drop(df.columns[11:],axis=1)
df2=df2.rename(columns={"Chromosome":"#CHROM","Position":"POS"})
df2.to_csv("OV-SMC_TopMT_VCFQ3OVER.vcf",sep="\t",index=False)
