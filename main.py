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
    files = [file for file in path.iterdir() if file.is_file()]
    for file in files:
        # solange nur file mode da ist ....
        CONFIG["file_path"] = str(file)
        print(f"processing: {CONFIG['file_path']}")
        try:
            data_loader = DataLoader(CONFIG)
            analyzer = Analyzer(data_loader, CONFIG)

            df = analyzer.occurrences_to_csv(index_col="phrase")
            # construct out path
            in_path = Path(CONFIG["file_path"])
            save_path = in_path.parent / "output" / in_path.name
            save_path = save_path.with_name(save_path.stem + "_processed.csv")
            df.to_csv(save_path, encoding="utf-8-sig")
        except TypeError as e:
            print(f"{e} | in file: {str(file)}")
