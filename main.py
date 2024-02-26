from pathlib import Path

import pandas as pd
from data_analysis import Analyzer, DataLoader
# supress pandas warnings
import warnings

from data_analysis.data_filter import PhraseCrossOverFilter

warnings.filterwarnings("ignore")

# init Configuration
CONFIG = {
    "file_path": "data/DE-Gerichtsurteile-NEG.xlsx",
    "plot_path": Path("imgs/test.png"),
    "drop_cols": ["Typ", "Label Obj. Moralwerte", "Label Subj. Moralwerte", "Label Kommunikative Funktionen",
                  "Spans Kommunikative Funktionen", "Label Protagonist:innen", "Spans Protagonist:innen",
                  "Label Explizite Forderungen", "Spans Explizite Forderung", "Label Implizite Forderungen",
                  "Spans Implizite Forderung"],
    "merge_cols": ["Spans Obj. Moralwerte", "Spans Subj. Moralwerte"],
    "mode": "dir",
}

if __name__ == '__main__':
    path = Path("data/output")
    files = [file for file in path.iterdir() if file.is_file() and file.name.startswith("FR")]
    data_stack = []
    data_loader = DataLoader(CONFIG)
    analyzer = Analyzer(data_loader, CONFIG)
    print(f"num files: {len(files)}")
    for file in files:
        print(file.name)
        df = pd.read_csv(file)
        data_stack.append(df)
    data_filter = PhraseCrossOverFilter
    analyzer.plot_phrases(data_stack, data_filter)
