import pandas as pd

def _clean(df):
    if "participant_id" in df:
        clean_df = df[df["participant_id"].notna()].dropna(how="all")
    else:
        clean_df = df.dropna(how="all")
    new_df = pd.DataFrame(clean_df.to_dict())
    return new_df

cancer_participant_disease = _clean(pd.read_csv("data/cancer_participant_disease.tsv", sep="\t"))
data_dictionary = _clean(pd.read_csv("data/data_dictionary.csv"))
death_details = _clean(pd.read_csv("data/death_details.tsv", sep="\t"))
hes_ae_subset = _clean(pd.read_csv("data/hes_ae_subset.csv"))
ons = _clean(pd.read_csv("data/ons.tsv", sep="\t"))
participant = _clean(pd.read_csv("data/participant.tsv", sep="\t"))

names = [
    "cancer_participant_disease",
    "data_dictionary",
    "death_details",
    "hes_ae_subset",
    "ons",
    "participant",
]