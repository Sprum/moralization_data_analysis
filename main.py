from pathlib import Path

from matplotlib import pyplot as plt

from data_analysis import Analyzer, DataLoader
# supress pandas warnings
import warnings

from data_analysis.data_filter import PhraseCrossOverFilter, MoralDistributionFilter, ConcatMultipleDataFrames, Void
from data_analysis.filter_sequence import FilterSequence

warnings.filterwarnings("ignore")

# init Configuration
CONFIG = {
    "file_path": "data/output/per_instance",
    "data_out_path": "data/imgs/phrases",
    "plot_path": Path("imgs/testings.png"),
    "drop_cols": ["Typ", "Label Obj. Moralwerte", "Label Subj. Moralwerte", "Label Kommunikative Funktionen",
                  "Spans Kommunikative Funktionen", "Label Protagonist:innen", "Spans Protagonist:innen",
                  "Label Explizite Forderungen", "Spans Explizite Forderung", "Label Implizite Forderungen",
                  "Spans Implizite Forderung"],
    "merge_cols": ["Spans Obj. Moralwerte", "Spans Subj. Moralwerte"],
}

data_dict = {
    "Gerichtsurteile": ["data\output\per_instance\DE-Gerichtsurteile-NEG_lemmatized.csv",
                        "data\output\per_instance\DE-Gerichtsurteile-POS_lemmatized.csv"],
    "Interviews": ["data\output\per_instance\DE-Interviews-NEG_lemmatized.csv",
                   "data\output\per_instance\DE-Interviews-POS_lemmatized.csv"],
    "Kommentare": ["data\output\per_instance\DE-Kommentare-NEG_lemmatized.csv",
                   "data\output\per_instance\DE-Kommentare-POS_lemmatized.csv"],
    "Leserbriefe": ["data/output/per_instance/DE-Leserbriefe-NEG_lemmatized.csv",
                    "data/output/per_instance/DE-Leserbriefe-POS_lemmatized.csv"],
    "Plenarprotokolle": ["data/output/per_instance/DE-Plenarprotokolle-NEG_lemmatized.csv",
                         "data/output/per_instance/DE-Plenarprotokolle-POS_lemmatized.csv"],
    "Sachbuecher": ["data/output/per_instance/DE-Sachbuecher-POS_lemmatized.csv"],
    "Wikipediadiskussionen": ["data/output/per_instance/DE_Wikipediadiskussionen_neg_compact_lemmatized.csv",
                              "data/output/per_instance/DE_Wikipediadiskussionen_pos_compact_lemmatized.csv"]
}

if __name__ == '__main__':
    data_loader = DataLoader.get_loader(CONFIG)
    analyzer = Analyzer(data_loader, CONFIG)
    analyzer.make_bar_chart(data_dict, Void)
