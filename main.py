import pandas as pd

from analyzer import Analyzer
from data_analysis.dataloader import DataLoader
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
}

data_loader = DataLoader(CONFIG)

analyzer = Analyzer(data_loader)

data_dict = analyzer._map_data('phrase_to_moral')
analyzer._make_csv(data_dict)

#
# unique_strings = list(set(string for strings_list in data_dict.values() for string in strings_list))
#
# # Initialize an empty DataFrame
# df = pd.DataFrame(index=unique_strings)
#
# # Populate the DataFrame
# for moral_value, strings_list in data_dict.items():
#     df[moral_value] = df.index.isin(strings_list).astype(int)
#
# # Replace NaN with 0
# df = df.fillna(0)
#
# # Optionally, convert index to a column
# df.reset_index(inplace=True)
#
# # Display the DataFrame
# print(df)
# df.to_csv("data/output/test.csv", index=False)
