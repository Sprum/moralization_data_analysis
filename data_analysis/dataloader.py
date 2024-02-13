from pathlib import Path

import pandas as pd
from pandas import DataFrame

MFT_SET = {"Care", "Harm", "Fairness", "Cheating", "Loyalty", "Betrayal", "Authority", "Subversion", "Purity",
           "Degradation", "Liberty",
           "Oppression", "OTHER"}


class DataLoader:
    """
    Class to load data and preprocess, eg. remove whitespace and quotation marks. Init with a Config dictionary.
    """

    def __init__(self, conf: dict) -> None:
        self.config = conf
        self.data_path = Path(self.config["file_path"])
        self.raw_data = self._read_data()
        self.data = None
        self.save_path = "output/" + self.config["file_path"].split(".")[0] + "_processed.csv"

    def load(self) -> DataFrame | list[DataFrame]:
        """
        Method to load, validate and process data. Can load dirs and files.
        :return: DataFrame | list[DataFrame]
        """
        path = self.data_path
        if path.is_dir():
            print(f"loading data from dir: {path}")
            data = []
            for file in path.iterdir():
                data_temp = pd.read_csv(file)
                data.append(data_temp)
            return data
        else:
            print(f"loading data from file: {path}")
            if not self._is_processed():
                print(f"processesing data: {path}")
                data = self._reformat()
                data = self._clean_data(data)
                data['moral_werte'] = data.apply(self._validate_split, axis=1)
                self.data = data
                return data

            else:
                print("Data already processed, continuing.")
                data = pd.read_csv(path)
                return data

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
        # merge data
        data['moral_werte'] = data.apply(self._merge_columns, axis=1)

        return data

    @staticmethod
    def _clean_data(data: DataFrame) -> DataFrame:
        """
        method to clean data from unnecessary whitespaces, hashes
        :param data: DataFrame
        :return: DataFrame
        """
        non_rows = []
        # iterate over rows
        for c_idx, content in data['moral_werte'].items():
            # check if content is none and skip row
            if not content:
                non_rows.append(c_idx)
                continue
            else:
                # iterate over list of strings of row
                for s_idx, string in enumerate(content):
                    # remove whitespaces at begin and end of str
                    string = string.strip()
                    # remove hashes
                    string = string.replace("#", "")
                    # remove quotation marks
                    clean_string = string.replace('"', '')
                    clean_string = clean_string.replace(u'\u201e', '')
                    clean_string = clean_string.replace(u'\u201c', '')
                    # update string in list
                    content[s_idx] = clean_string
                # update list in Series
                data["moral_werte"].iloc[c_idx] = content
        # drop na rows
        if non_rows:
            none_mask = data['moral_werte'].isnull()
            data = data.drop(data[none_mask].index)
        return data

    @staticmethod
    def _validate_split(row: pd.Series) -> pd.Series:
        """
        Validates and processes the 'moral_werte' column by concatenating list items based on specific conditions.

        Parameters:
        - row (pd.Series): A row of a Pandas DataFrame.

        Returns:
        - pd.Series: Processed 'moral_werte' column.
        """
        s_list = row['moral_werte']
        # Check if the list has more than one item
        if len(s_list) > 1:
            new_list = [s_list[0]]  # Initialize with the first item

            # Iterate over the remaining items in the list
            for idx, string in enumerate(s_list[1:], start=1):
                # Check if string was split on an unsafe semicolon
                if not any([string.startswith(moral_val) for moral_val in MFT_SET]):
                    # Concatenate with the previous item in the new list
                    new_list[-1] += "; " + string
                else:
                    # If safe, add as a separate entry in the new list
                    new_list.append(string)

            return new_list
        else:
            # If the list has only one item, return it unchanged
            return s_list

    @staticmethod
    def _merge_columns(row: pd.Series):
        """
        merges columns and splits on semicolons after evaluating they are eligible as separators and not part of the
        text span.
        :param row: pd.Series
        :return: pd.Series
        """
        if pd.isna(row['Spans Obj. Moralwerte']) and not pd.isna(row['Spans Subj. Moralwerte']):
            res_row = row['Spans Subj. Moralwerte'].split(";")

        elif not pd.isna(row['Spans Obj. Moralwerte']) and pd.isna(row['Spans Subj. Moralwerte']):
            res_row = row['Spans Obj. Moralwerte'].split(";")

        elif not pd.isna(row['Spans Obj. Moralwerte']) and not pd.isna(row['Spans Subj. Moralwerte']):
            res_row = row['Spans Obj. Moralwerte'].split(";") + row['Spans Subj. Moralwerte'].split(";")
        else:
            res_row = []
        return res_row

    @staticmethod
    def _check_semicolon(text: str) -> bool:
        """
        helper method to check whether a semicolon is present that should not be sliced at
        :return: bool
        """

        semicolon_count = 0
        value_count = 0
        semicolon_count = text.count(";")
        # no semicolon present -> nothing to slice carefully
        if semicolon_count == 0:
            return True
        # semicolon matches number of moral vals -> safe slicing on semicolons
        elif semicolon_count == value_count:
            return True
        # if semicolon_count != value_count: non separating semicolon as part of text span detected -> treat differently
        else:
            return False

    def _read_data(self) -> pd.DataFrame:
        """
        Method to read in xlsx files as DataFrame.
        :return: DataFrame of exel file as is
        """
        if not self.data_path.is_dir():
            try:
                if self.data_path.suffix != ".xlsx":
                    raw_data = pd.read_csv(self.data_path)
                    return raw_data
                else:
                    raw_data = pd.read_excel(self.data_path)
            except FileNotFoundError:
                self.data_path = input(f"File {self.config['file_path']} not present, please enter a valid path:")
                raw_data = self._read_data()
            return raw_data
        else:
            try:
                sample_file = next(self.data_path.iterdir())
                raw_data = pd.read_csv(sample_file)
                return raw_data
            except FileNotFoundError:
                self.data_path = input(f"File {self.config['file_path']} not present, please enter a valid path:")
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
