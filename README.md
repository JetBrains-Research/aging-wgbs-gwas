# Clone repo

Use `git clone git@aging-wgbs-gwas.git:JetBrains-Research/aging-wgbs-gwas.git` on comput server

# Prepare Data & Indexes:

* Data
   
   From  http://www.nealelab.is/uk-biobank download [UKBB GWAS Imputed v3 table](https://docs.google.com/spreadsheets/d/1kvPoupSzsSFBNSztMzl04xMoSC3Kcx3CrjVf4yBmESU/edit?ts=5b5f17db#gid=178908679)
  
   Save `UKBB GWAS Imputed v3 - File Manifest Release 20180731 - Manifest 201807.tsv` and provide as `gwas_table_path` in config

* Indexes
  
   Use USCS like `*.chrom.size` file, e.g. download from `wget http://hgdownload.soe.ucsc.edu/goldenPath/{genome}/bigZips/{genome}.chrom.sizes`

# Launch Locally
`snakemake --jobs 20 --use-conda --dry-run`

# Launch on LSF cluster:

## Prerequisites

Clone this repo to some directory, let's refer to it as `$PIPELINE_SRC`

1. Install snakemake profile for LSF from https://github.com/iromeo/generic-enhanced:

    Run container
    ```bash
    cd ~ && bsub -Is -G compute-martyomov -q general-interactive -a 'docker(biolabs/snakemake:5.10.0_conda4.8.2)' /bin/bash -l
    PIPELINE_WORKDIR=...
    PIPELINE_SRC=...
    ```
     
    To install this profile,
    ```bash
    mkdir -p ~/.config/snakemake
    cd ~/.config/snakemake
    cookiecutter https://github.com/iromeo/generic-enhanced.git
    ```

    Configure default options, e.g:
    * You've downloaded ~/.cookiecutters/generic before. Is it okay to delete and re-download it? [yes]: `yes`
    * profile: `lsf_wgbs`
    * cluster_system: `lsf`
    * submission_command_prefix: `cd $HOME &&`
    * default_job_group: `/your_username/wgbs`
    * default_queue: `general`
    * default docker: `biolabs/snakemake:5.10.0_conda4.8.2`
    * default_time_min: `20`
2. Add LSF queue for pipeline
    E.g. Add a queue with max 20 parallel jobs:
    ```bash
    bgadd -L 20 /your_username/wgbs
    ```
    Group status:
    ```bash
    bjgroup -s /your_username/wgbs
    ```
    To increase jobs number in existing queue use:
    ```bash
    bgmod -L 30 /your_username/wgbs 
    ```
3. Change/create `~/.condarc` file and replace `~/.conda/pkg` with path to disk with large quota
    E.g. `~/.condarc` could be:   
    ```yaml
    pkgs_dirs:
      - /opt/conda/pkgs
      - /some/big/storage/.conda/pkg
    ```
   
## Run

Pipeline could be launched in source dir for simplicity

Configure temp folder
```shell script
# run interactive container
bsub -cwd $HOME -Is -G compute-martyomov -q general-interactive -a 'docker(biolabs/snakemake:5.10.0_conda4.8.2)' /bin/bash -l
PIPELINE_SRC=...
PIPELINE_WORKDIR=$PIPELINE_SRC

# setup custom TMPDIR in pipeline workdir
mkdir -p "$PIPELINE_WORKDIR/tmp"
mkdir -p ~/docker_containers_envs
echo "__LSF_JOB_CUSTOM_TMPDIR__=$PIPELINE_WORKDIR/tmp" > ~/docker_containers_envs/$(basename $PIPELINE_WORKDIR).env
chmod a+r ~/docker_containers_envs/$(basename $PIPELINE_WORKDIR).env 
```

Run pipeline

```shell script
export PIPELINE_DOCKER_IMG='biolabs/snakemake:5.30.1_conda4.9.2_py37'
PIPELINE_SRC=...
PIPELINE_WORKDIR=$PIPELINE_SRC

export PIPELINE_LOG=$PIPELINE_WORKDIR/submission_01.log; LOCAL_CORES=4; LSF_DOCKER_ENV_FILE=~/docker_containers_envs/$(basename $PIPELINE_WORKDIR).env; bsub -cwd $HOME -n $LOCAL_CORES -G compute-martyomov -q general -oo $PIPELINE_LOG -R 'span[hosts=1]'  -a "docker($PIPELINE_DOCKER_IMG)" /bin/bash  -c "source /etc/bash.bashrc; cd $PIPELINE_WORKDIR; export TMPDIR=$PIPELINE_WORKDIR/tmp; snakemake -pr --use-conda --profile lsf_wgbs --jobscript ~/.config/snakemake/lsf_wgbs/lsf-jobscript.sh --local-cores $LOCAL_CORES --latency-wait 15 --restart-times 1 --jobs 200 --keep-going --dry-run"

tail -f $PIPELINE_LOG  | grep -e "steps" -e "Error" -e "Finished" -e "Submitted" -e "exited" -e "job summary" -e "usage summary" -e "DAG" -e "Exception" -e "Traceback"
```

Not all GWAS could be downloaded, in order to rerun and skip downloading step:
* Create GWAS list file: `find filtered_tsv -name '*.tsv' > filtered_tsv.list`
* Rerun snakemake command with additional argument `--config gwas_filtered_list_path='filtered_tsv.list'` 
