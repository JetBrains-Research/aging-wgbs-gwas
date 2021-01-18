# Clone repo

Use `git clone git@aging-wgbs-gwas.git:JetBrains-Research/aging-wgbs-gwas.git` on comput server

# Data

From  http://www.nealelab.is/uk-biobank download [UKBB GWAS Imputed v3 table](https://docs.google.com/spreadsheets/d/1kvPoupSzsSFBNSztMzl04xMoSC3Kcx3CrjVf4yBmESU/edit?ts=5b5f17db#gid=178908679)

Save `UKBB GWAS Imputed v3 - File Manifest Release 20180731 - Manifest 201807.tsv` and provide as `gwas_table_path` in config

# Indexes

Use USCS like `*.chrom.size` file, e.g. download from `wget http://hgdownload.soe.ucsc.edu/goldenPath/{genome}/bigZips/{genome}.chrom.sizes`

# Launch

`snakemake --jobs 20 --use-conda --dry-run`
