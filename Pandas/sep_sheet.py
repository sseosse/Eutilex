import pandas as pd
import os
from xlsxwriter import Workbook

writer = pd.ExcelWriter(f'MTAF.xlsx', engine='xlsxwriter')

raw=pd.read_excel('AF_Korean.xlsx',sheet_name=0)
hlaa=raw[raw["Allele"].str.contains("A")]
hlab=raw[raw["Allele"].str.contains("B")]
hlac=raw[raw["Allele"].str.contains("C")]

hlaa.to_excel(writer,sheet_name="A",index=False)
hlab.to_excel(writer,sheet_name="B",index=False)
hlac.to_excel(writer,sheet_name="C",index=False)
raw.to_excel(writer,sheet_name="unfiltered",index=False)
writer.save()
