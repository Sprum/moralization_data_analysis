import pandas as pd
from pandas import DataFrame


class DataLoader:
    """
    Class to load data and preprocess, eg. remove whitespace and quotationmarks. Init with a Config dictionary.
    """
    def __init__(self, conf: dict) -> None:
        self.config = conf
        self.raw_data = self._read_data()
        self.data = None
        self.save_path = "output/" + self.config["file_path"].split(".")[0] + "_processed.csv"

    def load(self) -> DataFrame:
        """
        Method to load, validate and process data.
        :return: None
        """
        if not self._is_processed():
            print("processesing data...")
            data = self._reformat()
            data = self._clean_data(data)
            self.data = data
            return data

        else:
            print("Data already processed, continuing.")

    def save(self) -> None:
        """
        save the processed data
        :return:
        """
        self.data.to_csv(self.save_path, index=False)

    def _reformat(self) -> DataFrame:
        """
        helper that drops specified cols and merges the specified ones.
        :return: pd.DataFrame clean of unnecessary cols

        """
        # drop cols
        data = self.raw_data.drop(self.config["drop_cols"], axis=1)
        data['moral_werte'] = data.apply(self._merge_columns, axis=1)
        return data

    @staticmethod
    def _clean_data(data: DataFrame) -> DataFrame:
        """
        method to clean data from unnecessary whitespaces, hashes
        :param data: DataFrame
        :return: DataFrame
        """
        # iterate over rows
        for c_idx, content in data['moral_werte'].items():
            # iterate over list of strings of row
            for s_idx, string in enumerate(content):
                # remove whitespaces at begin and end of str
                string = string.strip()
                # remove hashs
                string = string.replace("#", "")
                # remove Gänsefüßchen
                string = string.replace('"', '')
                # update string in list
                content[s_idx] = string
            # update list in Series
            data["moral_werte"].iloc[c_idx] = content
        return data

    @staticmethod
    def _merge_columns(row: pd.Series):
        """
        merges columns
        :param row: pd.Series
        :return: pd.Series
        """
        if pd.isna(row['Spans Obj. Moralwerte']) and not pd.isna(row['Spans Subj. Moralwerte']):
            return row['Spans Subj. Moralwerte'].split(";")
        elif not pd.isna(row['Spans Obj. Moralwerte']) and pd.isna(row['Spans Subj. Moralwerte']):
            return row['Spans Obj. Moralwerte'].split(";")
        elif not pd.isna(row['Spans Obj. Moralwerte']) and not pd.isna(row['Spans Subj. Moralwerte']):
            return row['Spans Obj. Moralwerte'].split(";") + row['Spans Subj. Moralwerte'].split(";")

    def _read_data(self) -> pd.DataFrame:
        """
        Method to read in xlsx files as DataFrame.
        :return: DataFrame of exel file as is
        """
        try:
            raw_data = pd.read_excel(self.config["file_path"])
        except FileNotFoundError:
            self.config["file_path"] = input(f"File {self.config['file_path']} not present, please enter a valid path:")
            raw_data = self._read_data()
        return raw_data

    def _is_processed(self) -> bool:
        """
        Helper to check whether or not a df has been processed yet by checking for cols that should be dropped.
        :return: bool
        """
        if "Label Obj. Moralwerte" in self.raw_data:
            return False
        return True

    def __repr__(self):
        return "DataManager object"
