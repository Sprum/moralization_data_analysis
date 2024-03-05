from pathlib import Path

import pandas as pd
from data_analysis import Analyzer, FileDataLoader
# supress pandas warnings
import warnings

from data_analysis.data_filter import MoralDistributionFilter, PhraseCrossOverFilter
from data_analysis.filter_sequence import FilterSequence

warnings.filterwarnings("ignore")

# init Configuration
CONFIG = {
    "file_path": "data/DE-Gerichtsurteile-NEG.xlsx",
    "drop_cols": ["Typ", "Label Obj. Moralwerte", "Label Subj. Moralwerte", "Label Kommunikative Funktionen",
                  "Spans Kommunikative Funktionen", "Label Protagonist:innen", "Spans Protagonist:innen",
                  "Label Explizite Forderungen", "Spans Explizite Forderung", "Label Implizite Forderungen",
                  "Spans Implizite Forderung"],
    "merge_cols": ["Spans Obj. Moralwerte", "Spans Subj. Moralwerte"],
    "mode": "dir",
}

if __name__ == "__main__":
    df = pd.read_csv("data/output/DE-Gerichtsurteile-POS_lemmatized.csv")
    sequence = FilterSequence(df, [PhraseCrossOverFilter])
    res = sequence.filter()
    print(res.iloc[5])
