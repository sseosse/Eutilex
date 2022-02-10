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
raw_path = main_path+"Sample_rawdata/"
#Threads
thread = "30"
########################################################################################

#Making directory 
def mkdir():
    os.chdir(sample_path)
    if sample_name not in os.listdir():
        for dir_name in dir_list:
            os.system(f"mkdir -p {sample_name}/{dir_name}")

#Trimming raw data
def trim():
    os.chdir(f"{sample_path}{sample_name}/{dir_list[0]}")
    fq2 = fq1.replace("_1.", "_2.")
    trim_log = fq1.replace("_1.fastq.gz", ".log")
    paired_fq1 = fq1.replace("fastq.gz", "paired.fq")
    paired_fq2 = fq2.replace("fastq.gz", "paired.fq")
    unpaired_fq1 = paired_fq1.replace("paired", "unpaired")
    unpaired_fq2 = paired_fq2.replace("paired", "unpaired")
    if trim_log not in os.listdir():
        cmd = f"/bin/java -jar {tool_path}trimmomatic-0.39/trimmomatic-0.39.jar \
PE \
-threads {thread} \
-phred33 {raw_path}{fq1} {raw_path}{fq2} {paired_fq1} {unpaired_fq1} {paired_fq2} {unpaired_fq2} \
AVGQUAL:30 \
LEADING:3 \
TRAILING:3 \
MINLEN:50 \
SLIDINGWINDOW:4:15 2> {trim_log}"
        print(cmd)
        os.system(cmd)

#Aligning trimmed data
def txd():
    os.chdir(f"{sample_path}{sample_name}/{dir_list[0]}")
    fq2 = fq1.replace("_1.", "_2.")
    paired_fq1 = fq1.replace("fastq.gz", "paired.fq")
    paired_fq2 = fq2.replace("fastq.gz", "paired.fq")
    if "align_summary.txt" not in os.listdir(f"{sample_path}{sample_name}/{dir_list[1]}"):
        cmd = f"{tool_path}tophat-2.1.1.Linux_x86_64/tophat \
--output-dir ../{dir_list[1]} \
--num-threads {thread} \
--mate-std-dev 56 \
--library-type fr-unstranded \
/home/oem/data/hg38/Homo_sapiens/NCBI/GRCh38/Sequence/Bowtie2Index/genome {paired_fq1} {paired_fq2}"
        print(cmd)
        os.system(cmd)

        cmd2 = f"samtools index ../{dir_list[1]}/accepted_hits.bam"
        print(cmd2)
        os.system(cmd2)

#Estimating expression
def cufflinks():
    os.chdir(f"{sample_path}{sample_name}/{dir_list[1]}")
    if f"{sample_name}_Cufflinks.log" not in os.listdir(f"{sample_path}{sample_name}/{dir_list[2]}"):
        cmd = f"{tool_path}cufflinks-2.2.1.Linux_x86_64/cufflinks \
--output-dir ../{dir_list[2]} \
--num-threads {thread} \
--library-type fr-unstranded \
--GTF /home/oem/data/hg38/GCA_000001405.15_GRCh38_full_analysis_set.refseq_annotation.gtf \
--multi-read-correct \
--max-mle-iterations 10000 \
--max-bundle-frags 5000000 \
--compatible-hits-norm \
accepted_hits.bam 2> ../{dir_list[2]}/{sample_name}_Cufflinks.log"
        print(cmd)
        os.system(cmd)


def wts():
	mkdir()
	trim()
	txd()
	cufflinks()

for raw in glob.glob(f"{raw_path}*-RNA_1.fastq.gz"):
    fq1 = os.path.basename(raw)
    sample_name = fq1.split("-RNA")[0]
    wts()

