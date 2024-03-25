from pathlib import Path

from data_analysis import Analyzer, DataLoader
# supress pandas warnings
import warnings

from data_analysis.data_filter import PhraseCrossOverFilter, MoralDistributionFilter

warnings.filterwarnings("ignore")

# init Configuration
CONFIG = {
    "file_path": "data/input/",
    "data_out_path": "data/input/merged",
    "plot_path": Path("imgs/all_moral_distribution.png"),
    "drop_cols": ["Typ", "Label Obj. Moralwerte", "Label Subj. Moralwerte", "Label Kommunikative Funktionen",
                  "Spans Kommunikative Funktionen", "Label Protagonist:innen", "Spans Protagonist:innen",
                  "Label Explizite Forderungen", "Spans Explizite Forderung", "Label Implizite Forderungen",
                  "Spans Implizite Forderung"],
    "merge_cols": ["Spans Obj. Moralwerte", "Spans Subj. Moralwerte"],
    "mode": "dir",
}

if __name__ == '__main__':

    file_names = [file.name.split(".")[0] + "_lemmatized.csv" for file in Path("data/input/").iterdir() if file.is_file()]

    data_loader = DataLoader.get_loader(CONFIG)
    analyzer = Analyzer(data_loader, CONFIG)
    df_stack = analyzer.occurrences_to_csv(index_col="phrase", aggregate=False)
    for i, df in enumerate(df_stack):
        path = "data/output/per_instance/" + file_names[i]
        df.to_csv(path)

    # i = 0
    # for df in df_stack:
    #     i += 1
    #     df.to_csv(CONFIG["data_out_path"]+f"/{str(i)}.csv")

    # path = Path("data/output")
    # files = [file for file in path.iterdir() if file.is_file() and file.name.startswith("DE")]
    # data_stack = []
    # data_loader = DataLoader.get_loader(CONFIG)
    # analyzer = Analyzer(data_loader, CONFIG)
    # print(f"num files: {len(files)}")
    # for file in files:
    #     print(file.name)
    #     df = pd.read_csv(file)
    #     data_stack.append(df)
    # data_filter = MoralDistributionFilter
    # analyzer.plot_phrases(data_stack, data_filter)
