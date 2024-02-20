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
    def filter(self) -> Series:
        """
        Method to filter Data based on criteria provided
        :param data:
        :return: Series
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

