from pathlib import Path

from data_analysis import Analyzer, DataLoader
# supress pandas warnings
import warnings

from data_analysis.data_filter import PhraseCrossOverFilter, MoralDistributionFilter

warnings.filterwarnings("ignore")

# init Configuration
CONFIG = {
    "file_path": "data/output/",
    "data_out_path": "data/imgs",
    "plot_path": Path("imgs/all_moral_distribution.png"),
    "drop_cols": ["Typ", "Label Obj. Moralwerte", "Label Subj. Moralwerte", "Label Kommunikative Funktionen",
                  "Spans Kommunikative Funktionen", "Label Protagonist:innen", "Spans Protagonist:innen",
                  "Label Explizite Forderungen", "Spans Explizite Forderung", "Label Implizite Forderungen",
                  "Spans Implizite Forderung"],
    "merge_cols": ["Spans Obj. Moralwerte", "Spans Subj. Moralwerte"],
}

if __name__ == '__main__':

    data_loader = DataLoader.get_loader(CONFIG)
    analyzer = Analyzer(data_loader, CONFIG)
    print(analyzer.data)

