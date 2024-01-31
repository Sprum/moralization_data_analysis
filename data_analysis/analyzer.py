from pathlib import Path

import pandas as pd
import spacy

from data_analysis.dataloader import DataLoader

MFT_SET = {"Care", "Harm", "Fairness", "Cheating", "Loyalty", "Betrayal", "Authority", "Subversion", "Purity",
           "Degradation", "Liberty",
           "Oppression", "OTHER"}


class Analyzer:
    """
    Class to analyze labeled data. Init with DatLoader and config dictionary.
    """

    def __init__(self, dataloader: DataLoader, config):
        self.data = dataloader.load()
        self.config = config
        self.nlp = self._nlp_factory()

    # TODO: add workflow to read in whole dir
    def occurrences_to_csv(self, mode: str = "file", **kwargs) -> pd.DataFrame:
        """
        get, transform and turn data in to csv. either a single file or a whole directory.
        :param mode: str: str | bool  -> specify if you want to create a csv from dir or file
        :param kwargs: set phrase to index of df with index_col="phrase"
        :return: DataFrame (or Error :))
        """
        if mode == "file":
            data_dict = self._map_data('phrase_to_moral')
            counted_vals = self._count_moral_vals(data_dict)
            df = self._make_csv(counted_vals, **kwargs)
            return df

        elif mode == "dir":
            print("to be implemented")
        else:
            raise ValueError(f"Unknown mode: {mode}\ntry 'file' or 'dir' instead")

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

    def _make_csv(self, counted_vals: list, save: bool = False, out_path: str = "data/output/test.csv",
                  index_col: str | bool = False) -> pd.DataFrame:
        """
        Helper method that takes a dict mapping phrases to labeled moral values and creates a Dataframe with the phrases
         and the respective number they were labeled.
        :param counted_vals: list
        :param save: bool
        :param index_col: str|bool
        :return: DataFrame
        """
        # create and order Dataframe
        order = ['phrase', 'Degradation', 'Care', 'Harm', 'Subversion', 'Fairness', 'Authority', 'Purity', 'Cheating',
                 'OTHER', 'Loyalty', 'Oppression', 'Betrayal', 'Liberty']
        df = pd.DataFrame(counted_vals)
        df.fillna(0)
        df = df[order]
        # optional: set phrases to index
        if index_col:
            index = True
            df.set_index(index_col, inplace=True)
        else:
            index = False
        # save if save true
        if save:
            df.to_csv(out_path, index=index)
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
            for idx, string in enumerate(s_list):
                # check if string was split on unsafe semicolon:
                if not any([string.startswith(moral_val) for moral_val in MFT_SET]):
                    print(s_list[idx - 1], string)
                # slice string for key and val (based on mode)
                sliced_str = string.split(":", maxsplit=1)
                key = sliced_str[key_index].strip()
                # lemmatize with stopword:
                if mode == "phrase_to_moral":
                    key = self._lemmatize(key)
                val = sliced_str[val_index].strip()
                # append data
                if key in data_dict:
                    data_dict[key].append(val)
                else:
                    data_dict[key] = [val]
        return data_dict

    def _nlp_factory(self):
        in_path = Path(self.config['file_path']).name
        if in_path.startswith("DE"):
            nlp = spacy.load('de_core_news_lg')
            return nlp
        elif in_path.startswith("EN"):
            nlp = spacy.load('en_core_web_lg')
            return nlp
        elif in_path.startswith("FR"):
            nlp = spacy.load('fr_core_news_lg')
            return nlp
        elif in_path.startswith("IT"):
            nlp = spacy.load('it_core_news_lg')
            return nlp
        else:
            print("unsupported language. Languages supported are: EN, DE, FR, IT")
            return None

    def _lemmatize(self, string: str):
        if self.nlp:
            doc = self.nlp(string)
            lemmatized_string = ' '.join([token.lemma_ for token in doc])
            return lemmatized_string
        else:
            raise ValueError("No NLP Model loaded; supported languages: EN, DE, FR, IT")
