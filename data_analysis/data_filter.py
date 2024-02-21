from abc import abstractmethod, ABC

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib as mpl
from pandas import DataFrame, Series


class DataFilter(ABC):
    """
    Data Filter Object that takes a DataFrame and returns a filtered Series.
    """

    def __init__(self, data: DataFrame, *args, **kwargs):
        self.data = data

    @abstractmethod
    def filter(self) -> Series | DataFrame:
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

    def filter(self) -> Series:
        cf = self.data.drop('phrase', axis=1)
        filtered_data = cf.sum()
        return filtered_data


class PhraseCrossOverFilter(DataFilter):
    """
    Filter for Filtering for phrases that occure in more than one moral value.
    :return: Series
    """

    def filter(self) -> DataFrame:
        df = self.data
        moral_columns = df.columns[1:]

        truth_table = (df[moral_columns] != 0).sum(axis=1) > 1
        cf = df[truth_table]
        return cf


if __name__ == "__main__":
    df = pd.read_csv("../data/output/DE-Interviews-NEG_lemmatized.csv")
    filter = PhraseCrossOverFilter(df)
    srs = filter.filter()
    print(srs)
