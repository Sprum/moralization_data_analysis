import re
from abc import abstractmethod, ABC
from typing import List

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib as mpl
from pandas import DataFrame, Series


class DataFilter(ABC):
    """
    Data Filter Object that takes a DataFrame and returns a filtered Series.
    """

    def __init__(self, data: DataFrame | Series | List, *args, **kwargs):
        self.data = data

    @abstractmethod
    def filter(self, *args, **kwargs) -> Series | DataFrame:
        """
        Method to filter Data based on criteria provided
        :param data:
        :return: Series or DataFrame
        """


class MoralDistributionFilter(DataFilter):
    """
    Filter for Filtering the Distribution of Moral Values in the DataFrame
    :return: Series
    """

    def filter(self, *args, **kwargs) -> Series:
        cf = self.data.drop('phrase', axis=1)
        filtered_data = cf.sum()
        return filtered_data


class PhraseCrossOverFilter(DataFilter):
    """
    Filter for Filtering for phrases that occure in more than one moral value.
    :return: Series
    """

    def filter(self, *args, **kwargs) -> DataFrame:
        df = self.data
        moral_columns = df.columns[1:]

        truth_table = (df[moral_columns] != 0).sum(axis=1) > 1
        cf = df[truth_table]
        return cf


class RegExFilter(DataFilter):
    """
    Filter to filter phrases with a Regex Pattern.
    Expects: "r_pattern" in kwargs
    """

    def filter(self, *args, **kwargs) -> list[Series]:
        r_pattern = kwargs.get("r_pattern")  # Get the regex pattern from kwargs

        if not r_pattern:
            raise ValueError("Regex pattern ('r_pattern') is required as kwarg.")

        # Apply regex pattern to the DataFrame
        matched_indices = self.data["phrase"].str.contains(r_pattern, flags=re.IGNORECASE, regex=True).astype(bool)

        # Filter the DataFrame based on matched indices
        filtered_df = self.data[matched_indices]

        return filtered_df


# Util Classes

class ConcatDataFrames(DataFilter):
    """
    deprecated :^)
    """
    def filter(self, df1, df2, **kwargs) -> DataFrame:
        res_df = pd.concat([df1, df2], **kwargs)
        return res_df


class ConcatMultipleDataFrames(DataFilter):
    """
    Adapter to concatenate a list of DataFrames to one DataFrame
    """
    def filter(self, *args, **kwargs) -> DataFrame:
        if not isinstance(self.data, list) or not all(isinstance(df, pd.DataFrame) for df in self.data):
            raise ValueError("The 'data' attribute must be a list of DataFrames.")

        if not self.data:
            raise ValueError("At least one DataFrame must be provided.")

        res_df = pd.concat(self.data)
        return res_df


class SumUpSeries(DataFilter):
    """Adapter to sum up a list of Series element-wise."""
    def filter(self, *args, **kwargs) -> Series:
        series = self.data
        res_srs = None
        for srs in series:
            if res_srs is None:
                res_srs = srs
            else:
                res_srs += srs
        return res_srs


class SeriesToDataFrameAdapter(DataFilter):
    """Adapter to convert a list of Series into a DataFrame."""
    def filter(self, *args, **kwargs) -> DataFrame:
        series_list = self.data
        return pd.concat(series_list, axis=1)


class DataFrameToSeriesList(DataFilter):
    """Adapter to convert a DataFrame into a list of Series."""
    def filter(self,  *args, **kwargs) -> List[Series]:
        df = self.data
        series_list = [df[col] for col in df.columns]
        return series_list


if __name__ == "__main__":
    df = pd.read_csv("../data/output/DE-Interviews-NEG_lemmatized.csv")
    filter = PhraseCrossOverFilter(df)
    srs = filter.filter()
    print(srs)
