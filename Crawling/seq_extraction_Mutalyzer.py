from urllib.request import urlopen
from selenium import webdriver
from bs4 import BeautifulSoup
import sys,os
import pandas as pd
from xlsxwriter import Workbook
from string import digits
sample_name = sys.argv[1]
os.chdir(f"/data/Neoantigen_samples/{sample_name}")

for at in ["A","T"]:
    sht = pd.read_excel(f'{sample_name}.xlsx', sheet_name=f'{sample_name}{at}_SNV')
    filtrow=sht.loc[sht['Corresponding Fold Change']>5]
    dropfiltrow = filtrow.drop_duplicates(['HGVSc'])
    dic={}
    for i in dropfiltrow['HGVSc']:
        hgvs=i
        mhtml = urlopen(f"https://mutalyzer.nl/name-checker?description={hgvs}")
        mutalyzer = BeautifulSoup(mhtml, "html.parser")
        seqlist=[]
        for RefMutseq in mutalyzer.find_all("pre"):
            if "b style" in str(RefMutseq):
                seqlist.append(str(RefMutseq))
        for j in seqlist:
            handseq=j.replace(' ','').replace('<ttstyle="color:#333;font-weight:normal">','').replace('<pre>','').replace('</pre>','').replace('</tt>','').split('<br/>')
            for k in handseq:
                if "bstyle" in k:
                    idx=int(handseq.index(k))
                    Fsq=handseq[idx-1]
                    Msq=handseq[idx].replace('<bstyle="color:#FF0000">','>').replace('</b>','<')
                    Lsq=handseq[idx+1]
                    extseq=Fsq+Msq+Lsq
                    table = str.maketrans('','',digits)
                    newextseq=extseq.translate(table)
                    mutidx=newextseq.index(">")
                    seq25=newextseq[mutidx-12:mutidx+15].replace('>','').replace('<','')
                    if i in dic:
                        if seq25 not in dic[i]:
                            dic[i].append(seq25)
                    else:
                        dic[i]=[seq25]
        
        for sub in mutalyzer.find_all(text=True):
            if "substitution" in sub:
                num=sub.split(" ")[-1]
        nhtml = f"https://www.ncbi.nlm.nih.gov/nuccore/{hgvs.split(':')[0]}"
        driver = webdriver.Chrome(executable_path='/home/oem/Downloads/chromedriver')
        driver.implicitly_wait(10)
        driver.get(nhtml)
        contents = driver.find_elements_by_class_name("ff_line")
        a=''
        for l in contents:
            a+=l.text.replace(" ","").strip()
        NTseq=a[int(num)-39:int(num)+38]
        driver.quit()
        if NTseq[38] == hgvs[-3].lower():
            MNTseq=NTseq[:38]+NTseq[38].replace(hgvs[-3].lower(),hgvs[-1].lower())+NTseq[39:]

        if NTseq not in dic[i]:
            dic[i].append(NTseq)

        if MNTseq not in dic[i]:
            dic[i].append(MNTseq)

    filtrow=filtrow.sort_values(by='Corresponding Fold Change',ascending=False)

    for x in range(0,len(filtrow)):
        filtrow.iloc[x,19]=dic[filtrow.iloc[x,11]][1]
        filtrow.iloc[x,20]=dic[filtrow.iloc[x,11]][0]
        filtrow.iloc[x,21]=dic[filtrow.iloc[x,11]][3]
        filtrow.iloc[x,22]=dic[filtrow.iloc[x,11]][2]

    filtrow.to_csv(f'{sample_name}{at}.SNVseq.tsv', index=False,sep="\t")

writer = pd.ExcelWriter(f'{sample_name}_neoang.xlsx', engine='xlsxwriter')
for ll in os.listdir(os.curdir):
    if not os.stat(ll).st_size==0 and ("seq" in ll or "II" in ll or "nonSNV"in ll):
        sheet = pd.read_csv(ll,delimiter='\t')
        sheet.to_excel(writer,sheet_name=f"{ll.split('.')[0]}_{ll.split('.')[-2]}",index=False)
writer.save()
