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
srd_path = main_path+"Sample_rawdata/"
#Threads
thread = "16"
########################################################################################

def HLAminer(file):
    time.sleep(0.5)
    os.chdir(main_path+'HLAminer_v1.4/data')
    if not "HLAminer_HPTASR.log" in os.listdir(sample_path+sample_name_spl+"/"+dir_list[3]):
        time.sleep(3600) #for waiting WES
        sample_name2 = sample_name.replace("_1.", "_2.")
        #Making link raw data
        cmd = f'ln -s {srd_path}{sample_name} .'
        cmd2 = f'ln -s {srd_path}{sample_name2} .'
        print(cmd)
        os.system(cmd)
        print(cmd2)
        os.system(cmd2)
        
        #Writing raw data name
        cmd3 = f'echo {sample_name} > patient.fof'
        cmd4 = f'echo {sample_name2} >> patient.fof'
        print(cmd3)
        os.system(cmd3)
        print(cmd4)
        os.system(cmd4)
        
        #Running HLAminer
        cmd5 = './HPTASRrnaseq_classI-II.sh'
        print(cmd5)
        os.system(cmd5)
        
        #Making copy result
        cmd6 = f'cp *_HPTASR.* {sample_path}{sample_name_spl}/{dir_list[3]}'
        print(cmd6)
        os.system(cmd6)

for file in glob.glob(f"{srd_path}*_1.fastq.gz"):
    sample_name = os.path.basename(file)
    sample_name_spl = sample_name.split("-RNA")[0]
    HLAminer(file)
