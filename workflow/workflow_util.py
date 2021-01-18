import pandas as pd

def load_gwas_data(path):
    df = pd.read_csv(path, sep="\t")
    gwas_file_id = []
    for phen, cmd in zip(df['Phenotype Code'], df['wget command']):
        if pd.isna(phen):
            # skip
            gwas_file_id.append("")
        else:
            chunks = cmd.split(" -O ")
            if len(chunks) != 2:
                raise AssertionError(f"Expected 2 chunks here, but was {len(chunks)} for: {cmd}")
            gwas_file_id.append(chunks[1].replace('.tsv.bgz', ''))

    df['gwas_file_id'] = gwas_file_id
    df = df[df['gwas_file_id'] != ""]
    df.set_index('gwas_file_id', drop=False, inplace=True)
    return df
