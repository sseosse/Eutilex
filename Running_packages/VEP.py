import os,glob

def VEP(file):
    os.chdir("/home/oem/Desktop/vep/mutectvep/passvep")
    cmd = f'/home/oem/Program/ensembl-vep/vep --force_overwrite --cache --format vcf --tab -i ../{vepname} -o {vepname_spl}.VEP.vcf --fork 32 --symbol --terms SO --tsl --hgvs --pick --refseq REFSEQ_MATCH --use_given_ref --plugin Frameshift --plugin Downstream --plugin Wildtype --fasta /data/hg38/Homo_sapiens_assembly38.fasta --dir_plugins /home/oem/.vep/Plugins'
    print(cmd)
    os.system(cmd)

for file in glob.glob("/home/oem/Desktop/vep/mutectvep/*.PASS.vcf"):
    vepname = os.path.basename(file)
    vepname_spl = vepname.split(".vcf")[0]
    VEP(file)
