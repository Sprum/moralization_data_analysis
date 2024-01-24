import pandas as pd

from data_analysis.dataloader import DataLoader

MFT_SET = {"Care", "Harm", "Fairness", "Cheating", "Loyalty", "Betrayal", "Authority", "Subversion", "Purity",
           "Degradation", "Liberty",
           "Oppression", "OTHER"}


class Analyzer:
    def __init__(self, dataloader: DataLoader):
        self.data = dataloader.load()

    # TODO: add workflow to read in whole dir
    def occurrences_to_csv(self, mode: str = "file") -> pd.DataFrame:
        if mode == "file":
            data_dict = self._map_data('phrase_to_moral')
            counted_vals = self._count_moral_vals(data_dict)
            df = self._make_csv(counted_vals)
        elif mode == "dir":
            print("to be implemented")
        else:
            raise ValueError(f"Unknown mode: {mode}\ntry 'file' or 'dir' instead")
        return df

    def _count_moral_vals(self, data_dict: dict) -> list[dict[str:str | str:int]]:
        """
        Helper method to count moral values for each phrase
        :param data_dict: dictionary containing phrases mapping to lists of all the moral values that they were labeled with.
        :return: list of format [{"phrase": phrase | moral_value: count}
        """
        # count moral values in data dict
        list_of_phrases = []
        for phrase, moral_val_list in data_dict.items():
            moral_val_counter = {mv: 0 for mv in MFT_SET}
            # iter over moral_val strings
            for occurrence in moral_val_list:
                # iter over list of moral values and count them
                if occurrence in MFT_SET:
                    moral_val_counter[occurrence] += 1
            moral_val_counter["phrase"] = phrase
            # append dict to list
            list_of_phrases.append(moral_val_counter)
        return list_of_phrases

    def _make_csv(self, counted_vals: list, save: bool = True, index: str | bool = False) -> pd.DataFrame:
        """
        Helper method that takes a dict mapping phrases to labeled moral values and creates a Dataframe with the phrases
         and the respective number they were labeled.
        :param counted_vals: list
        :param save: bool
        :param index: str|bool
        :return: DataFrame
        """
        # create and order Dataframe
        order = ['phrase', 'Degradation', 'Care', 'Harm', 'Subversion', 'Fairness', 'Authority', 'Purity', 'Cheating',
                 'OTHER', 'Loyalty', 'Oppression', 'Betrayal', 'Liberty']
        df = pd.DataFrame(counted_vals)
        df.fillna(0)
        df = df[order]
        # optional: set phrases to index
        if index:
            df.set_index(index, inplace=True)
        # save if save true
        if save:
            df.to_csv("data/output/test.csv", index=False)
        return df

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
