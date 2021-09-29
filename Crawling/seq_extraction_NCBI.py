from urllib.request import urlopen
from selenium import webdriver
from bs4 import BeautifulSoup
import sys,os
import pandas as pd
from xlsxwriter import Workbook
from string import digits
import time
a=pd.read_excel("All-OV_MT100_seq.xlsx")
b=a.drop_duplicates(['Gene'])
genelist=b['Gene'].tolist()
dic={}
dic2={}
for sample_name in genelist:
    mhtml = f"https://www.genenames.org/tools/search/#!/?query={sample_name}"
    ll=''
    driver = webdriver.Chrome(executable_path='/home/Program/chromedriver')
    driver.get(mhtml)
    time.sleep(5)
    contents = driver.find_elements_by_class_name("hgnc-id")
    nn=contents[0].text
    s1="".join(i for i in nn if i.isdigit())
    mhtml2 = f"https://www.genenames.org/data/gene-symbol-report/#!/hgnc_id/HGNC:{s1}"
    driver.get(mhtml2)
    time.sleep(5)
    driver.implicitly_wait(10)
    contents = driver.find_elements_by_class_name("td ")
    for j in contents:
        if "NM"  in j.text:
            l=j.text.split(" ")[0]
            mhtml3 = f"https://www.ncbi.nlm.nih.gov/nuccore/{l}"
            driver.get(mhtml3)
            time.sleep(5)
            conte = driver.find_elements_by_class_name("feature")
            for m in conte:
                if "translation" in m.text:
                    ll+=m.text.replace("\n","").replace(" ","").strip()
                else:
                    continue
            seq=ll.split("tion=")[1].replace('"','')
            dic[sample_name]=seq
            dic2[sample_name]=l
            driver.quit()
            break
for i in b['Gene']:
    a.loc[a['Gene']==i,'Sequence AA']=dic[i]
    a.loc[a['Gene']==i,'Transcript ID']=dic2[i]

for i in a['Sequence AA']:
    a.loc[a['Sequence AA']==i,'Sequence length']=len(i)


for i in range(len(a)):
    mut=a.iloc[i]["Mutation"]
    pos="".join(k for k in mut.split("*")[0] if k.isdigit())
    if int(pos)<14:
        aa=a.iloc[i]['Sequence AA'][:int(pos)+13]
    elif int(pos)+13 > a.iloc[i]["Sequence length"]:
        aa=a.iloc[i]['Sequence AA'][int(pos)-14:]
    else:
        aa=a.iloc[i]['Sequence AA'][int(pos)-14:int(pos)+13]
    a.loc[i,'WT Sequence AA 27']=aa

a.to_excel("All-OV_MT100_ExtSeq.xlsx",index=0)
