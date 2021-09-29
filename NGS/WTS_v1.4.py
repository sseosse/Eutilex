import glob, os, sys
import threading, time
from multiprocessing import Process

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

#Making directory 
def Mkdir(file):
    os.chdir(sample_path)
    if sample_name_spl not in os.getcwd():
        for dir_name in dir_list:
            os.system("mkdir -p "+sample_name_spl+"/"+dir_name)

#Trimming raw data
def Trimmomatic(file):
    os.chdir(sample_path+sample_name_spl+"/"+dir_list[0])
    id_right = sample_name.replace("_1.", "_2.")
    id_log = sample_name.replace("_1.fastq.gz", ".log")
    id_left_output_paired = sample_name.replace("_1.fastq.gz", "_1.paired.fq")
    id_right_output_paired = id_left_output_paired.replace("_1.", "_2.")
    id_left_output_unpaired = id_left_output_paired.replace("paired", "unpaired")
    id_right_output_unpaired = id_right_output_paired.replace("paired", "unpaired")
    if not id_log in os.listdir(os.curdir):
        cmd = f'java -jar {tool_path}trimmomatic-0.39/trimmomatic-0.39.jar PE -threads {thread} -phred33 {srd_path}{sample_name} {srd_path}{id_right} {id_left_output_paired} {id_left_output_unpaired} {id_right_output_paired} {id_right_output_unpaired} AVGQUAL:30 LEADING:3 TRAILING:3 MINLEN:50 SLIDINGWINDOW:4:15 2> {id_log}'
        print(cmd)
        os.system(cmd)

#Aligning trimmed data
def Align(file):
    os.chdir(sample_path+sample_name_spl+"/"+dir_list[0])
    R1_file = sample_name_spl+"-RNA_1.paired.fq"
    R2_file = R1_file.replace("_1.","_2.")
    if not "align_summary.txt" in os.listdir(sample_path+sample_name_spl+"/"+dir_list[1]):
        cmd = f'{tool_path}tophat-2.1.1.Linux_x86_64/tophat --output-dir ../02.Align --num-threads {thread} --mate-std-dev 56 --library-type fr-unstranded /home/oem/data/hg38/Homo_sapiens/NCBI/GRCh38/Sequence/Bowtie2Index/genome {R1_file} {R2_file}'
        print(cmd)
        os.system(cmd)

        cmd2 = 'samtools index ../02.Align/accepted_hits.bam'
        print(cmd2)
        os.system(cmd2)

#Estimating expression
def Cufflinks(file):
	os.chdir(sample_path+sample_name_spl+"/"+dir_list[1])
	if not f"{sample_name_spl}_Cufflinks.log" in os.listdir(sample_path+sample_name_spl+"/"+dir_list[2]):
		cmd = f'{tool_path}cufflinks-2.2.1.Linux_x86_64/cufflinks --output-dir ../{dir_list[2]} --num-threads {thread} --library-type fr-unstranded --GTF /home/oem/data/hg38/GCA_000001405.15_GRCh38_full_analysis_set.refseq_annotation.gtf --multi-read-correct --max-mle-iterations 10000 --max-bundle-frags 5000000 --compatible-hits-norm accepted_hits.bam 2> ../{dir_list[2]}/{sample_name_spl}_Cufflinks.log'
		print(cmd)
		os.system(cmd)


def Main(file):
	Mkdir(file)
	Trimmomatic(file)
	Align(file)
	Cufflinks(file)

for file in glob.glob(f"{srd_path}*_1.fastq.gz"):
    sample_name = os.path.basename(file)
    sample_name_spl = sample_name.split("-RNA")[0]
    Main(file)

