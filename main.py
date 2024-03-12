from pathlib import Path

import pandas as pd
from data_analysis import Analyzer, FileDataLoader, DataLoader
# supress pandas warnings
import warnings

from data_analysis.data_filter import PhraseCrossOverFilter, MoralDistributionFilter

warnings.filterwarnings("ignore")

# init Configuration
CONFIG = {
    "file_path": "data/",
    "data_out_path": "data/asdf",
    "plot_path": Path("imgs/all_moral_distribution.png"),
    "drop_cols": ["Typ", "Label Obj. Moralwerte", "Label Subj. Moralwerte", "Label Kommunikative Funktionen",
                  "Spans Kommunikative Funktionen", "Label Protagonist:innen", "Spans Protagonist:innen",
                  "Label Explizite Forderungen", "Spans Explizite Forderung", "Label Implizite Forderungen",
                  "Spans Implizite Forderung"],
    "merge_cols": ["Spans Obj. Moralwerte", "Spans Subj. Moralwerte"],
    "mode": "dir",
}

if __name__ == '__main__':

    data_loader = DataLoader.get_loader(CONFIG)
    analyzer = Analyzer(data_loader, CONFIG)
    df_stack = analyzer.occurrences_to_csv(index_col="phrase")

    i = 0
    for df in df_stack:
        i += 1
        df.to_csv(CONFIG["data_out_path"]+f"/{str(i)}.csv")
    # path = Path("data/output")
    # files = [file for file in path.iterdir() if file.is_file() and file.name.startswith("IT")]
    # data_stack = []
    # data_loader = DataLoader.get_loader(CONFIG)
    # analyzer = Analyzer(data_loader, CONFIG)
    # print(f"num files: {len(files)}")
    # for file in files:
    #     print(file.name)
    #     df = pd.read_csv(file)
    #     data_stack.append(df)
    # data_filter = MoralDistributionFilter
    # analyzer.make_piecharts(data_stack, data_filter)
