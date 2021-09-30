import glob, os, sys                                                                           
import threading, time
###############################################################################Variable table
#Directory list
dir_list = ['01.Trimmomatic','02.BAM','03.GATK','04.VCF','05.VEP']
#Main path
main_path  = "/home/oem/data/WES/"
#Tools path
tool_path = "/home/Program/"
#Path of Sample analysis
sample_path = main_path+"Sample_analysis/"
#Path of Sample raw data
srd_path = main_path+"Sample_rawdata/"
#Threads
thread = "16"
#Ram
ram = "20G"
#############################################################################################

#Making directory 
def Mkdir(file):
    os.chdir(sample_path)
    if sample_name_spl not in os.getcwd():
        for dir_name in dir_list:
            os.system("mkdir -p "+sample_name_spl+"/"+dir_name)

#Raw data trimming
def Trimmomatic(file):
    os.chdir(sample_path+sample_name_spl+"/"+dir_list[0])
    id_right = sample_name.replace("_1.", "_2.")
    id_log = sample_name.replace("_1.fastq.gz", ".log")
    id_left_output_paired = sample_name.replace("_1.fastq.gz", "_1.paired.fq")
    id_right_output_paired = id_left_output_paired.replace("_1.", "_2.")
    id_left_output_unpaired = id_left_output_paired.replace("paired", "unpaired")
    id_right_output_unpaired = id_right_output_paired.replace("paired", "unpaired")
    if not id_log in os.listdir(os.curdir):
        cmd = f'java -jar {tool_path}trimmomatic-0.39/trimmomatic-0.39.jar PE -threads {thread} -phred33 {srd_path}{sample_name} {srd_path}{id_right} {id_left_output_paired} {id_left_output_unpaired} {id_right_output_paired} {id_right_output_unpaired} ILLUMINACLIP:{tool_path}trimmomatic-0.39/adapters/TruSeq3-PE.fa:2:30:10:2:KeepBothReads LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:50 2> {id_log}'
        print(cmd)
        os.system(cmd)

#Alignment
def BWA(file):
    os.chdir(sample_path)
    sample_dirs = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d)]
    for sample_dir in sample_dirs:
        os.chdir(sample_path+sample_dir+"/"+dir_list[0])
        for id_left_paired in glob.glob("*_1.paired.fq"):
            id_right_paired = id_left_paired.replace("_1.", "_2.")
            id_sam = id_right_paired.split("_2.paired")[0]+".sam"
            id_bam = id_sam.replace('.sam','.sorted.bam')
            if id_bam not in os.listdir(sample_path+sample_dir+"/"+dir_list[1]):
                cmd = f"{tool_path}bwa-0.7.17/bwa mem -t {thread} -k 50 /home/oem/data/hg38/Homo_sapiens_assembly38.fasta {id_left_paired} {id_right_paired} > {sample_path+sample_dir+'/'+dir_list[1]+'/'+id_sam}"
                print(cmd)
                os.system(cmd)

#Sam to sorted bam
def BAM(file):
    os.chdir(sample_path)
    sample_dirs = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d)]
    for sample_dir in sample_dirs:
        os.chdir(sample_path+sample_dir+"/"+dir_list[1])
        for id_sam in glob.glob("*.sam"):
            id_sorted_bam = id_sam.replace(".sam",".sorted.bam")
            if id_sorted_bam not in os.listdir(os.curdir):
                cmd = f"{tool_path}samtools-1.12/samtools view -bS -@ {thread} {id_sam} | {tool_path}samtools-1.12/samtools sort -@ {thread} -o {id_sorted_bam}"
                print(cmd)
                os.system(cmd)

#Add readgroup
def RG(file):
    os.chdir(sample_path)
    sample_dirs = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d)]
    for sample_dir in sample_dirs:
        os.chdir(sample_path+sample_dir+"/"+dir_list[1])
        for id_bam in glob.glob("*sorted.bam"):
            RG_bam = id_bam.replace(".bam",".RG.bam")
            RG_log = id_bam.replace(".bam",".RG.log")
            if RG_bam not in os.listdir(os.curdir):
                cmd = f"{tool_path}gatk-4.1.8.1/gatk --java-options '-Xmx{ram} -XX:+UseParallelGC -XX:ParallelGCThreads={thread}' AddOrReplaceReadGroups -SO coordinate --CREATE_INDEX true -I {id_bam} -O {RG_bam} -ID SH -LB WES -PL illumina -PU OV -SM {id_bam.split('-WES')[0]} 2> {RG_log}"
                print(cmd)
                os.system(cmd)

#Mark duplicates
def MarkDuplicates(file):
    os.chdir(sample_path)
    sample_dirs = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d)]
    for sample_dir in sample_dirs:
        os.chdir(sample_path+sample_dir+"/"+dir_list[1])
        for RG_bam in glob.glob("*.RG.bam"):
            marked_bam = RG_bam.replace(".RG.bam",".RG.dedup.bam")
            marked_log = RG_bam.replace(".RG.bam",".RG.dedup.log")
            marked_mtr = RG_bam.replace(".RG.bam",".RG.marked.dup.metrics.txt")
            if marked_bam not in os.listdir(sample_path+sample_dir+"/"+dir_list[2]):
                cmd = f"{tool_path}gatk-4.1.8.1/gatk --java-options '-Xmx{ram} -XX:+UseParallelGC -XX:ParallelGCThreads={thread}' MarkDuplicates -I {RG_bam} -O ../{dir_list[2]}/{marked_bam} -M ../{dir_list[2]}/{marked_mtr} --VALIDATION_STRINGENCY SILENT -ASO coordinate --REMOVE_DUPLICATES --CREATE_INDEX true 2> ../{dir_list[2]}/{marked_log}"
                print(cmd)
                os.system(cmd)

#Must make VCF indexing
#Indexing example
#/home/oem/Program/gatk-4.1.8.1/gatk --java-options '-Xmx4G -XX:+UseParallelGC -XX:ParallelGCThreads=4' IndexFeatureFile --input resources_broad_hg38_v0_1000G_phase1.snps.high_confidence.hg38.vcf.gz

#Base recalibration + apply
def BQSR(file):
    os.chdir(sample_path)
    sample_dirs = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d)]
    for sample_dir in sample_dirs:
        os.chdir(sample_path+sample_dir+"/"+dir_list[2])
        for marked_bam in glob.glob("*RG.dedup.bam"):
            bqsr_table = marked_bam.replace("dedup.bam","dedup.recal_data.table")
            bqsr_log = marked_bam.replace("dedup.bam","dedup.bqsr.log")
            if bqsr_log not in os.listdir(os.curdir):
                cmd1 = f"{tool_path}gatk-4.1.8.1/gatk --java-options '-Xmx{ram} -XX:+UseParallelGC -XX:ParallelGCThreads={thread}' BaseRecalibrator -I {marked_bam} -R /home/oem/data/hg38/Homo_sapiens_assembly38.fasta --known-sites /home/oem/data/hg38/1000G_phase1.snps.high_confidence.hg38.vcf.gz --known-sites /home/oem/data/hg38/Mills_and_1000G_gold_standard.indels.hg38.vcf.gz -O {bqsr_table} 2> {bqsr_log}"
                print(cmd1)
                os.system(cmd1)
			    
                bqsr_bam = marked_bam.replace("RG.dedup.bam","RG.dedup.recal.bam")
                applybqsr_log = bqsr_log.replace("bqsr.log","applybqsr.log")
                cmd2 = f"{tool_path}gatk-4.1.8.1/gatk --java-options '-Xmx{ram} -XX:+UseParallelGC -XX:ParallelGCThreads={thread}' ApplyBQSR -I {marked_bam} -O {bqsr_bam} -bqsr {bqsr_table} 2> {applybqsr_log}"
                print(cmd2)
                os.system(cmd2)

                cmd3 = f"rm ../02.BAM/*.sam"
                print(cmd3)
                os.system(cmd3)

#Variant calling
def Mutect(file):
    os.chdir(sample_path)
    sample_dirs = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d)]
    for sample_dir in sample_dirs:
        if "-T" in sample_dir:
            os.chdir(sample_path+sample_dir+"/"+dir_list[2])
            for recal_bam in glob.glob("*.recal.bam"):
                tumor_name = recal_bam.split("-WES")[0]
                norm_name = tumor_name.split("-")[0]+"-N"
                norm_recal_bam = recal_bam.replace(tumor_name,norm_name)
                vc_log = tumor_name+".mutect2.log"
                unfilt = vc_log.replace(".log",".unfiltered.vcf")
                os.chdir(sample_path+sample_dir+"/"+dir_list[3])
                if vc_log not in os.listdir(os.curdir):
                    cmd1 = f"{tool_path}gatk-4.1.8.1/gatk --java-options '-Xmx{ram} -XX:+UseParallelGC -XX:ParallelGCThreads={thread}' Mutect2 -R /home/oem/data/hg38/Homo_sapiens_assembly38.fasta -I ../{dir_list[2]}/{recal_bam} -I {sample_path}{norm_name}/{dir_list[2]}/{norm_recal_bam} -normal {norm_name} -pon /home/oem/data/hg38/somatic-hg38_1000g_pon.hg38.vcf.gz --germline-resource /home/oem/data/hg38/somatic-hg38_af-only-gnomad.hg38.vcf.gz --ignore-itr-artifacts --af-of-alleles-not-in-resource 0.0000025 --disable-read-filter MateOnSameContigOrNoMappedMateReadFilter --bam-output {tumor_name}.mutect2.bam -O {unfilt} 2> {vc_log}"
                    print(cmd1)
                    os.system(cmd1)

                    #Filter mutect call
                    uf_file = tumor_name+".mutect2.unfiltered.vcf"
                    fmc_log = tumor_name+"_filtermutectcalls.log"
                    f_file = uf_file.replace(".unfiltered","")
                    cmd2 = f"{tool_path}gatk-4.1.8.1/gatk --java-options '-Xmx{ram} -XX:+UseParallelGC -XX:ParallelGCThreads={thread}' FilterMutectCalls --max-alt-allele-count 5 -R /home/oem/data/hg38/Homo_sapiens_assembly38.fasta -V {uf_file} -O {f_file} 2> {fmc_log}"
                    print(cmd2)
                    os.system(cmd2)

                    #"PASS" extraction
                    pass_file = f_file.replace(".vcf",".passed.vcf")
                    cmd3 = f"{tool_path}bcftools-1.10.2/bin/bcftools view -f 'PASS' {f_file} > {pass_file}"
                    print(cmd3)
                    os.system(cmd3)

		
def VEP(file):
    os.chdir(sample_path)
    sample_dirs = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d)]
    for sample_dir in sample_dirs:
        os.chdir(sample_path+sample_dir+"/"+dir_list[3])
        for passed_vcf in glob.glob("*.passed.vcf"):
            vep_vcf = passed_vcf.replace(".vcf",".VEP.vcf")
            if vep_vcf not in os.listdir(sample_path+sample_dir+"/"+dir_list[4]):
                cmd = f"{tool_path}ensembl-vep/vep --force_overwrite --cache --dir_cache /home/oem/.vep/ --format vcf --vcf -i {passed_vcf} -o ../{dir_list[4]}/{vep_vcf} --fork 32 --symbol --terms SO --tsl --hgvs --pick --refseq REFSEQ_MATCH --use_given_ref --plugin Downstream --plugin Wildtype --plugin Frameshift --fasta /home/oem/data/hg38/Homo_sapiens_assembly38.fasta --dir_plugins /home/oem/.vep/Plugins"
                print(cmd)
                os.system(cmd)

def Main(file):
    Mkdir(file)
    Trimmomatic(file)
    BWA(file)
    BAM(file)
    RG(file)
    MarkDuplicates(file)
    BQSR(file)
    Mutect(file)
    VEP(file)


for file in glob.glob(f"{srd_path}*_1.fastq.gz"):
    sample_name = os.path.basename(file)
    sample_name_spl = sample_name.split("-WES")[0]
    Main(file)

