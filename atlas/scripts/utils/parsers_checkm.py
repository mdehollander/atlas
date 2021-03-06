
import pandas as pd
import os
import warnings

def read_checkm_output(taxonomy_table, completness_table):

    c_df = pd.read_csv(completness_table, index_col=0,sep='\t')[
        ["Completeness", "Contamination", "Strain heterogeneity"]
    ]
    t_df = pd.read_csv(taxonomy_table, index_col=0,sep='\t')[
        [
            "# unique markers (of 43)",
            "# multi-copy",
            "Insertion branch UID",
            "Taxonomy (contained)",
            "Taxonomy (sister lineage)",
            "GC",
            "Genome size (Mbp)",
            "Gene count",
            "Coding density",
        ]
    ]
    df = pd.concat([c_df, t_df], axis=1)
    return df


def load_checkm_tax(checkm_taxonomy_file):

    checkmTax= pd.read_table(checkm_taxonomy_file,index_col=0)

    checkmTax = checkmTax['Taxonomy (contained)']

    if checkmTax.isnull().any():
        warnings.warn("Some samples have no taxonomy asigned based on checkm. Samples:\n"+ \
                    ', '.join(checkmTax.index[checkmTax.isnull()])
                    )
        checkmTax= checkmTax.dropna().astype(str)

    checkmTax= pd.DataFrame(list(  checkmTax.apply(lambda s: s.split(';'))),
                       index=checkmTax.index)

    checkmTax.columns=['kindom','phylum','class','order','family','genus','species']
    return checkmTax
