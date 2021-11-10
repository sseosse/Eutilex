import pandas as pd

ty="T"
fb=pd.read_excel(f"samplename_freebayes_{ty}.xlsx")
m2=pd.read_excel(f"samplename_mutect2_{ty}.xlsx")
vd=pd.read_excel(f"samplename_vardict_{ty}.xlsx")
vs=pd.read_excel(f"samplename_varscan_{ty}.xlsx")

mg=pd.merge(left=fb, right=m2, how="left", on=["Chromosome","Position","ID","REF","ALT"])
mg2=pd.merge(left=mg, right=vd, how="left", on=["Chromosome","Position","ID","REF","ALT"])
mg3=pd.merge(left=mg2, right=vs, how="left", on=["Chromosome","Position","ID","REF","ALT"])
fn=mg3.iloc[:,[0,1,3,4,11,50,95,141,187]]
#fn.columns =['HLA type','ECfq','AA2fq','MCfq','SAIfq','HSCAfq','CHfq']
#f2=fn.fillna(0)
fn.to_excel("OV-SMC-T_vc_mutation.xlsx",index=0)
