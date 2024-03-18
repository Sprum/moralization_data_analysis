import re
from typing import Type, Union, List

import pandas as pd
from pandas import DataFrame, Series

from data_analysis.data_filter import DataFilter, RegExFilter, DataFrameToSeriesList, ConcatMultipleDataFrames


class FilterSequence:
    """
    A class to manage a sequence of data filters to be applied to a DataFrame.

    Parameters:
    - data (DataFrame): The input DataFrame to be filtered.
    - filter_stack (list[Type[DataFilter]]): A list of DataFilter classes representing the sequence of filters to be applied.

    Methods:
    - __call__(self, *args, **kwargs): Executes the filter sequence on the provided DataFrame.

    Example Usage:
    ```python
    # Assuming df is your DataFrame
    filter_sequence = FilterSequence(df, [MoralDistributionFilter, PhraseCrossOverFilter])

    # Execute the filters in sequence
    result_df = filter_sequence()

    # Display the result
    print(result_df)
    ```
    """

    def __init__(self, data: DataFrame | Series | List, filter_stack: List[Type[DataFilter]]):
        """
        Initializes a FilterSequence object.

        Parameters:
        - :data:  DataFrame Series or List of those: The input Data to be filtered.
        - filter_stack (list[Type[DataFilter]]): A list of DataFilter classes representing the sequence of filters to be applied.
        """
        self.data = data
        self.filter_stack = filter_stack

    def filter(self, *args, **kwargs) -> Union[DataFrame, Series]:
        """
         Executes the filter sequence on the provided DataFrame
         Returns:
         - DataFrame: The filtered DataFrame.
         """
        result = self.data

        for data_filter in self.filter_stack:
            result = data_filter(result).filter(*args, **kwargs)

        return result


if __name__ == "__main__":
    df = pd.read_csv("E:\Coding\moralization\data\output\DE-Gerichtsurteile-NEG_lemmatized.csv")
    df2 = pd.read_csv("E:\Coding\moralization\data\output\DE-Kommentare-NEG_lemmatized.csv")
    df3 = pd.read_csv("E:\Coding\moralization\data\output\DE-Leserbriefe-NEG_lemmatized.csv")
    dfs = [df, df2, df3]
    r_pat = r'freiheit'

    for d in dfs:
        print(len(d))
    seq = FilterSequence(dfs, [ConcatMultipleDataFrames])

    outp = seq.filter(r_pattern=r_pat)
    print(outp)
