import pandas as pd

from data_analysis.dataloader import DataLoader

MFT_SET = {"Care", "Harm", "Fairness", "Cheating", "Loyalty", "Betrayal", "Authority", "Subversion", "Purity", "Degradation", "Liberty",
           "Oppression", "OTHER"}


class Analyzer:
    def __init__(self, dataloader: DataLoader):
        self.data = dataloader.load()

    def q_and_d(self):
        data_dict = self._map_data('moral_to_phrase')
        for key, val in data_dict.items():
            # print(len(val))
            pass
        print(data_dict)
        # return self._make_csv(self._map_data('moral_to_phrase'))

    def _make_csv(self, data_dict: dict):
        unique_strings = set(data_dict.keys())
        cols = list(MFT_SET).sort()
        #cols= cols.sort()
        df = pd.DataFrame(index=list(unique_strings), columns=cols)
        print(df)

    def _map_data(self, mode: str) -> dict[str: list]:
        """
        Helper method to process data DataFrame into a dictionary.
        :param mode: str; options:
        - 'phrase_to_moral': Target format: {word/phrase: [moral, values]}
        - 'moral_to_phrase': Target format: {moral value: [word/phrase]}
        :return: dict
        """
        data = self.data["moral_werte"]
        # index factory or error based on mode
        if mode == "phrase_to_moral":
            key_index, val_index = 1, 0
        elif mode == "moral_to_phrase":
            key_index, val_index = 0, 1
        else:
            raise ValueError(f"Unknown mode: '{mode}'. consider using either 'phrase_to_moral' or 'moral_to_phrase'")
        # init dict
        data_dict = {}
        # iter over list in Series
        for s_list in data:
            # iter over string in list
            for string in s_list:
                # slice string for key and val (based on mode)
                sliced_str = string.split(":", maxsplit=1)
                key = sliced_str[key_index].strip()
                val = sliced_str[val_index].strip()
                # append data
                if key in data_dict:
                    data_dict[key].append(val)
                else:
                    data_dict[key] = [val]
        return data_dict
