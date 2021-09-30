import os,sys, fileinput, glob

thread = "60"

working_path = "/extradisk/bcbio_working"

def Runbcbio(sample_name):
    os.chdir(f"{working_path}/final")
    result_dir = f"{sample_name}-tumor"
    if result_dir not in os.listdir(os.curdir):
        os.chdir(f"{working_path}/work")
        os.system(f"mkdir {sample_name}_work")
        os.chdir(f"{sample_name}_work")
        cmd=f"bcbio_nextgen.py ../../config/{sample_name}.yaml -n {thread}"
        print(cmd)
        os.system(cmd)

def MakingYaml(sample_name):
    os.chdir(f"{working_path}/config")
    yaml_file = f"{sample_name}.yaml"
    if yaml_file not in os.listdir(os.curdir):
        #os.system(f"cp example_SMC.yaml {sample_name}.yaml")
        os.system(f"cp example_YUHS.yaml {sample_name}.yaml")
        for line in fileinput.input(f'{sample_name}.yaml', inplace = True):
            #if "SMC_00" in line:
                #line = line.replace("SMC_00", sample_name)
            if "YUHS_00" in line:
                line = line.replace("YUHS_00", sample_name)
            if "batch: batch" in line:
                line = line.replace("batch: batch", f"batch: {sample_name}")
            sys.stdout.write(line)
        Runbcbio(sample_name)

def Main(sample_name):
    MakingYaml(sample_name)

for raw in glob.glob(f"{working_path}/input/*T-WES_1.fastq.gz"):
    sample_name=os.path.basename(raw).split("-T-")[0]
    Main(sample_name)
