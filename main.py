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
    "file_path": "data/output/",
    "data_out_path": "data/imgs/phrases",
    "plot_path": Path("imgs/testings.png"),
    "drop_cols": ["Typ", "Label Obj. Moralwerte", "Label Subj. Moralwerte", "Label Kommunikative Funktionen",
                  "Spans Kommunikative Funktionen", "Label Protagonist:innen", "Spans Protagonist:innen",
                  "Label Explizite Forderungen", "Spans Explizite Forderung", "Label Implizite Forderungen",
                  "Spans Implizite Forderung"],
    "merge_cols": ["Spans Obj. Moralwerte", "Spans Subj. Moralwerte"],
}

if __name__ == '__main__':

    data_loader = DataLoader.get_loader(CONFIG)
    analyzer = Analyzer(data_loader, CONFIG)

    ax = analyzer.plotter.make_bar_chart(analyzer.data, ConcatMultipleDataFrames)
    plt.show()