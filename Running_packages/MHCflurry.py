import pandas as pd
import os

kr=pd.read_excel("HLAlist_KR_final.xlsx")
mt=pd.read_excel("All-OV_MT100_Mutseq.xlsx")
#mt=pd.read_excel("WTtoMT3.xlsx")
al=''
for i in kr["Allele"]:
    i="HLA-"+i
    al=al+" "+i

msl=''
for j in mt["MT Sequence AA 27"]:
    msl=msl+" "+j

os.environ['TF_CPP_MIN_LOG_LEVEL'] ='2'
cmd=f"mhcflurry-predict-scan --alleles{al} --sequences{msl} --out ./result11.csv"
print(cmd)
os.system(cmd)
