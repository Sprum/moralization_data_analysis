from pathlib import Path

import pandas as pd
from data_analysis import Analyzer, DataLoader
# supress pandas warnings
import warnings
warnings.filterwarnings("ignore")

# init Configuration
CONFIG = {
    "file_path": "data/DE-Gerichtsurteile-NEG.xlsx",
    "plot_path": Path("imgs/DE_moral_distribution.png"),
    "drop_cols": ["Typ", "Label Obj. Moralwerte", "Label Subj. Moralwerte", "Label Kommunikative Funktionen",
                  "Spans Kommunikative Funktionen", "Label Protagonist:innen", "Spans Protagonist:innen",
                  "Label Explizite Forderungen", "Spans Explizite Forderung", "Label Implizite Forderungen",
                  "Spans Implizite Forderung"],
    "merge_cols": ["Spans Obj. Moralwerte", "Spans Subj. Moralwerte"],
    "mode": "dir",
}

if __name__ == '__main__':
    path = Path("data/output")
    files = [file for file in path.iterdir() if file.is_file() and file.name.startswith('DE')]
    data_stack = []
    data_loader = DataLoader(CONFIG)
    analyzer = Analyzer(data_loader, CONFIG)
    for file in files:

        df = pd.read_csv(file)
        data_stack.append(df)

    analyzer.make_piecharts(data_stack)
