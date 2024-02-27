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

    def __init__(self, data: DataFrame | Series, *args, **kwargs):
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


class ConcatDataFrames(DataFilter):

    def filter(self, df1, df2, **kwargs) -> DataFrame:
        res_df = pd.concat([df1, df2], **kwargs)
        return res_df


class SumUpSeries(DataFilter):

    def filter(self, series_stack: list[Series], *args, **kwargs) -> Series:
        res_srs = None
        for srs in series_stack:
            if res_srs is None:
                res_srs = srs
            else:
                res_srs += srs
        return res_srs


if __name__ == "__main__":
    df = pd.read_csv("../data/output/DE-Interviews-NEG_lemmatized.csv")
    filter = PhraseCrossOverFilter(df)
    srs = filter.filter()
    print(srs)
