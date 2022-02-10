
import glob, os, sys                                                                           

###############################################################################Variable table
#Directory list
dir_list = ['01.Trimmomatic','02.BAM','03.GATK','04.VCF','05.VEP']
#Main path
main_path  = "/home/oem/data/WES/"
#Tool path
tool_path = "/home/Program/"
#Analysis path
sample_path = main_path+"Sample_analysis/"
#Raw data path
raw_path = main_path+"Sample_rawdata/"
#Thread
thread = "16"
#Ram
ram = "20G"
#############################################################################################

#Making directories
def mkdir():
    os.chdir(sample_path)
    if sample_name not in os.listdir():
        for dir_name in dir_list:
            os.system(f"mkdir -p {sample_name}/{dir_name}")

#Trimming fastq
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
ILLUMINACLIP:{tool_path}trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10:2:KeepBothReads \
LEADING:3 \
TRAILING:3 \
SLIDINGWINDOW:4:15 \
MINLEN:50 2> {trim_log}"
        print(cmd)
        os.system(cmd)

#Aligning trimmed fastq
def bwa():
    os.chdir(f"{sample_path}{sample_name}/{dir_list[1]}")
    sam = sample_name_type+".sam"
    bam = sam.replace(".sam",".sorted.bam")
    if bam not in os.listdir():
        os.chdir(f"{sample_path}{sample_name}/{dir_list[0]}")
        for paired_fq1 in glob.glob("*_1.paired.fq"):
            paired_fq2 = paired_fq1.replace("_1.", "_2.")
            cmd = f"{tool_path}bwa-0.7.17/bwa mem \
-t {thread} \
-k 50 \
/home/oem/data/hg38/Homo_sapiens_assembly38.fasta \
{paired_fq1} {paired_fq2} > {sample_path}{sample_name}/{dir_list[1]}/{sam}"
            print(cmd)
            os.system(cmd)

#Sam to sorted bam
def bam():
    os.chdir(f"{sample_path}{sample_name}/{dir_list[1]}")
    sam = sample_name_type+".sam"
    sorted_bam = sam.replace(".sam",".sorted.bam")
    if sorted_bam not in os.listdir():
        cmd = f"{tool_path}samtools-1.12/samtools view \
-bS -@ {thread} {sam} | \
{tool_path}samtools-1.12/samtools sort \
-@ {thread} \
-o {sorted_bam}"
        print(cmd)
        os.system(cmd)

#Add readgroup
def rg():
    os.chdir(f"{sample_path}{sample_name}/{dir_list[1]}")
    rg_log = sample_name_type+".RG.log"
    sorted_bam = sample_name_type+".sorted.bam"
    if rg_log not in os.listdir():
        rg_bam = sorted_bam.replace(".bam",".RG.bam")
        cmd = f"{tool_path}gatk-4.1.8.1/gatk --java-options \
'-Xmx{ram} \
-XX:+UseParallelGC \
-XX:ParallelGCThreads={thread}' \
AddOrReplaceReadGroups \
-SO coordinate \
--CREATE_INDEX true \
-I {sorted_bam} \
-O {rg_bam} \
-ID SH \
-LB WES \
-PL illumina \
-PU OV \
-SM {sample_name} 2> {rg_log}"
        print(cmd)
        os.system(cmd)

#Mark duplicates
def dedup():
    os.chdir(f"{sample_path}{sample_name}/{dir_list[1]}")
    rg_bam=sample_name_type+".sorted.RG.bam"
    dedup_bam = rg_bam.replace(".bam",".dedup.bam")
    dedup_log = rg_bam.replace(".bam",".dedup.log")
    dedup_mtr = rg_bam.replace(".bam",".dedup_metrics.txt")
    if dedup_log not in os.listdir(f"../{dir_list[2]}"):
        cmd = f"{tool_path}gatk-4.1.8.1/gatk --java-options \
'-Xmx{ram} \
-XX:+UseParallelGC \
-XX:ParallelGCThreads={thread}' \
MarkDuplicates \
-I {rg_bam} \
-O ../{dir_list[2]}/{dedup_bam} \
-M ../{dir_list[2]}/{dedup_mtr} \
--VALIDATION_STRINGENCY SILENT \
-ASO coordinate \
--REMOVE_DUPLICATES \
--CREATE_INDEX true 2> ../{dir_list[2]}/{dedup_log}"
        print(cmd)
        os.system(cmd)

#Must make VCF indexing
#Indexing example
#/home/oem/Program/gatk-4.1.8.1/gatk --java-options '-Xmx4G -XX:+UseParallelGC -XX:ParallelGCThreads=4' IndexFeatureFile --input resources_broad_hg38_v0_1000G_phase1.snps.high_confidence.hg38.vcf.gz

#Base recalibration + apply
def bqsr():
    os.chdir(f"{sample_path}{sample_name}/{dir_list[2]}")
    dedup_bam = sample_name_type+".sorted.RG.dedup.bam" 
    bqsr_table = dedup_bam.replace(".bam",".recal_data.table")
    bqsr_log = dedup_bam.replace(".bam",".bqsr.log")
    if bqsr_log not in os.listdir():
        cmd1 = f"{tool_path}gatk-4.1.8.1/gatk --java-options \
'-Xmx{ram} \
-XX:+UseParallelGC \
-XX:ParallelGCThreads={thread}' \
BaseRecalibrator \
-I {dedup_bam} \
-R /home/oem/data/hg38/Homo_sapiens_assembly38.fasta \
--known-sites /home/oem/data/hg38/1000G_phase1.snps.high_confidence.hg38.vcf.gz \
--known-sites /home/oem/data/hg38/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz \
-O {bqsr_table} 2> {bqsr_log}"
        print(cmd1)
        os.system(cmd1)
			    
        bqsr_bam = dedup_bam.replace(".bam",".recal.bam")
        applybqsr_log = bqsr_log.replace("bqsr.log","applybqsr.log")
        cmd2 = f"{tool_path}gatk-4.1.8.1/gatk --java-options \
'-Xmx{ram} \
-XX:+UseParallelGC \
-XX:ParallelGCThreads={thread}' \
ApplyBQSR \
-I {dedup_bam} \
-O {bqsr_bam} \
-bqsr {bqsr_table} 2> {applybqsr_log}"
        print(cmd2)
        os.system(cmd2)

        cmd3 = f"rm ../{dir_list[1]}/*.sam"
        print(cmd3)
        os.system(cmd3)

#Variant calling
def mutect2():
    os.chdir(f"{sample_path}{sample_name}/{dir_list[3]}")
    t_name = sample_name
    n_name = t_name.split("-")[0]+"-N"
    t_bqsr_bam = sample_name_type+".sorted.RG.dedup.recal.bam"
    n_bqsr_bam = t_bqsr_bam.replace(t_name,n_name)
    vc_log = t_name+".mutect2.log"
    uf_vcf = vc_log.replace(".log",".unfiltered.vcf")
    if vc_log not in os.listdir():
        cmd1 = f"{tool_path}gatk-4.1.8.1/gatk --java-options \
'-Xmx{ram} \
-XX:+UseParallelGC \
-XX:ParallelGCThreads={thread}' \
Mutect2 \
-R /home/oem/data/hg38/Homo_sapiens_assembly38.fasta \
-I ../{dir_list[2]}/{t_bqsr_bam} \
-I {sample_path}{n_name}/{dir_list[2]}/{n_bqsr_bam} \
-normal {n_name} \
-pon /home/oem/data/hg38/somatic-hg38_1000g_pon.hg38.vcf.gz \
--germline-resource /home/oem/data/hg38/somatic-hg38_af-only-gnomad.hg38.vcf.gz \
--ignore-itr-artifacts \
--af-of-alleles-not-in-resource 0.0000025 \
--disable-read-filter MateOnSameContigOrNoMappedMateReadFilter \
--bam-output {t_name}.mutect2.bam \
-O {uf_vcf} 2> {vc_log}"
        print(cmd1)
        os.system(cmd1)

        #Filter mutect call
        fmc_log = t_name+"_filtermutectcalls.log"
        vcf = uf_vcf.replace(".unfiltered","")
        cmd2 = f"{tool_path}gatk-4.1.8.1/gatk --java-options \
'-Xmx{ram} \
-XX:+UseParallelGC \
-XX:ParallelGCThreads={thread}' \
FilterMutectCalls \
--max-alt-allele-count 5 \
-R /home/oem/data/hg38/Homo_sapiens_assembly38.fasta \
-V {uf_vcf} \
-O {vcf} 2> {fmc_log}"
        print(cmd2)
        os.system(cmd2)

        #"PASS" extraction
        pass_vcf = vcf.replace(".vcf",".passed.vcf")
        cmd3 = f"{tool_path}bcftools-1.10.2/bin/bcftools view \
-f 'PASS' \
{vcf} > {pass_vcf}"
        print(cmd3)
        os.system(cmd3)

		
def vep():
    os.chdir(f"{sample_path}{sample_name}/{dir_list[4]}")
    pass_vcf = sample_name+".mutect2.passed.vcf"    
    vep_vcf = pass_vcf.replace("passed.vcf","passed.VEP.vcf")
    if vep_vcf not in os.listdir():
        cmd = f"{tool_path}ensembl-vep/vep \
--force_overwrite \
--cache \
--dir_cache /home/oem/.vep/ \
--format vcf \
--vcf -i ../{dir_list[3]}/{pass_vcf} \
-o {vep_vcf} \
--fork 32 \
--symbol \
--terms SO \
--tsl \
--hgvs \
--pick \
--refseq REFSEQ_MATCH \
--use_given_ref \
--plugin Downstream \
--plugin Wildtype \
--plugin Frameshift \
--fasta /home/oem/data/hg38/Homo_sapiens_assembly38.fasta \
--dir_plugins /home/oem/.vep/Plugins"
        print(cmd)
        os.system(cmd)

def wes():
    mkdir()
    trim()
    bwa()
    bam()
    rg()
    dedup()
    bqsr()

def vc():
    mutect2()
    vep()


for raw in glob.glob(f"{raw_path}*-N-WES_1.fastq.gz"):
    fq1 = os.path.basename(raw)
    sample_name = fq1.split("-WES")[0]
    sample_name_type = fq1.split("_1.")[0]
    wes()

for raw in glob.glob(f"{raw_path}*-T-WES_1.fastq.gz"):
    fq1 = os.path.basename(raw)
    sample_name = fq1.split("-WES")[0]
    sample_name_type = fq1.split("_1.")[0]
    wes()
    vc()
