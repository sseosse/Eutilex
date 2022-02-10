import glob, os, sys
import threading, time

##########################################################################Variable table
#Directoty list
dir_list = ['01.Trimmomatic','02.Align','03.Cufflinks','04.HLAtyping']
#Main path
main_path  = "/home/oem/data/WTS/"
#Tools path
tool_path = "/home/Program/"
#Path of Sample analysis
sample_path = main_path+"Sample_analysis/"
#Path of Sample raw data
raw_path = main_path+"Sample_rawdata/"
#Threads
thread = "16"
########################################################################################

def hlaminer():
    time.sleep(0.5)
    os.chdir(f"{main_path}HLAminer_v1.4/data")
    if "HLAminer_HPTASR.log" not in os.listdir(f"{sample_path}{sample_name}/{dir_list[3]}"):
        time.sleep(3600)
        fq2 = fq1.replace("_1.", "_2.")
       
        #Making link raw data
        cmd2 = f'ln -s {raw_path}{fq1} {raw_path}{fq2} .'
        print(cmd2)
        os.system(cmd2)
        
        #Writing raw data name
        cmd3 = f'echo {fq1} > patient.fof'
        cmd4 = f'echo {fq2} >> patient.fof'
        print(cmd3)
        os.system(cmd3)
        print(cmd4)
        os.system(cmd4)
        
        #Running HLAminer
        cmd5 = './HPTASRrnaseq_classI.sh'
        print(cmd5)
        os.system(cmd5)
        
        #Making copy result
        cmd6 = f'cp *_HPTASR.* {sample_path}{sample_name}/{dir_list[3]}'
        print(cmd6)
        os.system(cmd6)

for raw in glob.glob(f"{raw_path}*_1.fastq.gz"):
    fq1 = os.path.basename(raw)
    sample_name = fq1.split("-RNA")[0]
    hlaminer()
