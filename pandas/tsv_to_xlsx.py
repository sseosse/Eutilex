import glob, os
import pandas as pd

for file in glob.glob("/home/oem/Desktop/tsv/*.tsv"):
    tsv_name=os.path.basename(file)
    tsv_name_spt=tsv_name.split(".")[0]
    tsv = pd.read_csv(f"{tsv_name}",sep='\t',header=None)
    tsv.to_excel(f"{tsv_name_spt}.xlsx",index=0,header=None)
