from pathlib import Path

import pandas as pd
from data_analysis import Analyzer, DataLoader
# supress pandas warnings
import warnings
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

if __name__ == '__main__':
    path = Path("data")
    print(path.is_dir())
    files = [file for file in path.iterdir() if file.is_file()]
    for file in files:
        CONFIG["file_path"] = str(file)
        data_loader = DataLoader(CONFIG)
        analyzer = Analyzer(data_loader, CONFIG)

        df = analyzer.occurrences_to_csv(index_col="phrase")

