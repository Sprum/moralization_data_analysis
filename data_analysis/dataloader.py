from abc import ABC, abstractstaticmethod, abstractmethod
from pathlib import Path
from typing import List

import pandas as pd
from pandas import DataFrame, Series

MFT_SET = {"Care", "Harm", "Fairness", "Cheating", "Loyalty", "Betrayal", "Authority", "Subversion", "Purity",
           "Degradation", "Liberty",
           "Oppression", "OTHER"}

CONFIG = {
    "file_path": "../data/",
    "data_out_path": "../data/output",
    "plot_path": Path("imgs/all_moral_distribution.png"),
    "drop_cols": ["Typ", "Label Obj. Moralwerte", "Label Subj. Moralwerte", "Label Kommunikative Funktionen",
                  "Spans Kommunikative Funktionen", "Label Protagonist:innen", "Spans Protagonist:innen",
                  "Label Explizite Forderungen", "Spans Explizite Forderung", "Label Implizite Forderungen",
                  "Spans Implizite Forderung"],
    "merge_cols": ["Spans Obj. Moralwerte", "Spans Subj. Moralwerte"],
    "mode": "dir",
}


class DataLoaderInterface(ABC):
    @abstractmethod
    def __init__(self, conf: dict) -> None:
        pass

    @abstractmethod
    def load(self) -> DataFrame | list[DataFrame]:
        pass

    @abstractmethod
    def save(self) -> None:
        pass

    @abstractmethod
    def _reformat(self) -> DataFrame:
        pass

    @staticmethod
    @abstractmethod
    def _clean_data(data: DataFrame) -> DataFrame:
        pass

    @staticmethod
    @abstractmethod
    def _validate_split(row: Series) -> Series:
        pass

    @staticmethod
    @abstractmethod
    def _merge_columns(row: Series) -> Series:
        pass

    @abstractmethod
    def _read_data(self) -> DataFrame:
        pass

    @abstractmethod
    def _is_processed(self) -> bool:
        pass

    @abstractmethod
    def __repr__(self):
        return "DataManager object"


class DataLoader:
    @classmethod
    def get_loader(cls, config: dict):
        path = Path(config["file_path"])
        if path.is_dir():
            return DirDataLoader(config)
        else:
            return FileDataLoader(config)


class FileDataLoader(DataLoaderInterface):
    """
    Class to load data and preprocess, eg. remove whitespace and quotation marks. Init with a Config dictionary.
    """

    def __init__(self, conf: dict) -> None:
        self.config = conf
        self.data_path = Path(self.config["file_path"])
        self.raw_data = self._read_data()
        self.data = None
        self.save_path = self.config["data_out_path"] + "_processed.csv"

    def load(self) -> DataFrame:
        """
        Method to load, validate and process data. Can load files.
        :return: DataFrame | list[DataFrame]
        """
        path = self.data_path
        # for data in something
        data_stack = []

        print(f"loading data from file: {path}")
        if self._is_processed():
            print("Data already processed, continuing.")
            data = pd.read_csv(path)
            self.data = data

        else:
            print(f"processesing data: {path}")
            data = self._reformat(self.raw_data)
            data = self._clean_data(data)
            data['moral_werte'] = data.apply(self._validate_split, axis=1)
            self.data = data

        return data

    def save(self) -> None:
        """
        save the processed data
        :return:
        """
        self.data.to_csv(self.save_path, index=False)

    def _reformat(self, raw_data) -> DataFrame:
        """
        helper that drops specified cols and merges the specified ones.
        :return: pd.DataFrame clean of unnecessary cols

        """
        # drop cols
        data = raw_data.drop(self.config["drop_cols"], axis=1)
        # merge data
        data['moral_werte'] = data.apply(self._merge_columns, axis=1)

        return data

    @staticmethod
    def _clean_data(data: DataFrame) -> DataFrame:
        """
        Method to clean data from unnecessary whitespaces, hashes
        :param data: DataFrame
        :return: DataFrame
        """
        # Remove unnecessary whitespaces, hashes, and quotation marks from the 'moral_werte' column
        data['moral_werte'] = data['moral_werte'].apply(
            lambda content: [
                string.strip().replace("#", "").replace('"', '').replace(u'\u201e', '').replace(u'\u201c', '') for
                string in content] if content else content
        )

        # Drop rows with empty 'moral_werte'
        data = data.dropna(subset=['moral_werte'])

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
    def _merge_columns(row: Series):
        """
        merges columns and splits on semicolons after evaluating they are eligible as separators and not part of the
        text span.
        :param row: Series
        :return: Series
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

        try:
            if self.data_path.suffix != ".xlsx":
                raw_data = pd.read_csv(self.data_path)
                return raw_data
            else:
                raw_data = pd.read_excel(self.data_path)
        except FileNotFoundError:
            self.data_path = Path(input(f"File {self.config['file_path']} not present, please enter a valid path:"))
            raw_data = self._read_data()
        return raw_data

    def _is_processed(self) -> bool:
        """
        Helper to check whether a df has been processed yet by checking for cols that should be dropped. Naiv
        implementation: check for column labels that shouldn't be present.
        :return: bool
        """
        if "Label Obj. Moralwerte" in self.raw_data:
            return False
        return True

    def __repr__(self):
        return "DataManager object for files"


class DirDataLoader(DataLoaderInterface):
    """
    Class to load data and preprocess, eg. remove whitespace and quotation marks. Init with a Config dictionary.
    """

    def __init__(self, conf: dict) -> None:
        self.config = conf
        self.data_path = Path(self.config["file_path"])
        self.raw_data = self._read_data()
        self.data = None
        self.save_path = self.config["data_out_path"] + "_processed.csv"

    def load(self) -> List[DataFrame]:
        """
        Method to load, validate and process data. Can load dirs and files.
        :return: DataFrame | list[DataFrame]
        """
        path = self.data_path
        files = [file for file in path.iterdir() if file.is_file()]
        print(f"loading data from dir: {path}")
        data = []
        if self._is_processed():
            for file in files:
                print(f"loading data from file: {file}")
                data_temp = pd.read_csv(file)
                data.append(data_temp)
        else:
            for raw_data in self.raw_data:
                print(f"processesing data...")
                data_temp = self._reformat(raw_data)
                data_temp = self._clean_data(data_temp)
                data_temp['moral_werte'] = data_temp.apply(self._validate_split, axis=1)
                data.append(data_temp)
        return data

    def save(self) -> None:
        """
        save the processed data
        :return:
        """
        for df in self.data:
            save_path = self.save_path + df.name
            df.to_csv(save_path, index=False)

    def _reformat(self, raw_data: DataFrame) -> DataFrame:
        """
        helper that drops specified cols and merges the specified ones.
        :return: pd.DataFrame clean of unnecessary cols
        """
        # drop cols
        data = raw_data.drop(self.config["drop_cols"], axis=1)
        # merge data
        data['moral_werte'] = data.apply(self._merge_columns, axis=1)
        return data

    @staticmethod
    def _validate_split(row: Series) -> Series:
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
    def _clean_data(data: DataFrame) -> DataFrame:
        """
        method to clean data from unnecessary whitespaces, hashes
        :param data: DataFrame
        :return: DataFrame
        """
        # Remove unnecessary whitespaces, hashes, and quotation marks from the 'moral_werte' column
        data['moral_werte'] = data['moral_werte'].apply(
            lambda content: [
                string.strip().replace("#", "").replace('"', '').replace(u'\u201e', '').replace(u'\u201c', '') for
                string in content] if content else content
        )

        # Drop rows with empty 'moral_werte'
        data = data.dropna(subset=['moral_werte'])

        return data

    @staticmethod
    def _merge_columns(row: Series):
        """
        merges columns and splits on semicolons after evaluating they are eligible as separators and not part of the
        text span.
        :param row: Series
        :return: Series
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

    def _is_processed(self) -> bool:
        """
        Helper to check whether or not a df has been processed yet by checking for cols that should be dropped.
        :return: bool
        """

        if "Label Obj. Moralwerte" in next(iter(self.raw_data)):
            return False
        return True

    def _read_data(self) -> List[DataFrame]:
        """
        Method to read in xlsx files as DataFrame.
        :return: DataFrame of exel file as is
        """
        raw_data = []
        path = Path(self.data_path)
        files = [file for file in path.iterdir() if file.is_file()]
        for file in files:
            try:
                if file.suffix != ".xlsx":
                    temp_data = pd.read_csv(file)
                    raw_data.append(temp_data)
                else:
                    temp_data = pd.read_excel(file)
                    raw_data.append(temp_data)
            except FileNotFoundError:
                self.data_path = Path(input(f"File {self.config['file_path']} not present, please enter a valid path:"))
                self._read_data()
        return raw_data

    def __repr__(self):
        return "DataManager object for dirs"


if __name__ == "__main__":
    dl = DataLoader.get_loader(CONFIG)
    print(dl)
