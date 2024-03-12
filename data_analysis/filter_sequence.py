from typing import Type

import pandas as pd
from pandas import DataFrame

from data_analysis.data_filter import DataFilter


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

    def __init__(self, data: DataFrame, filter_stack: list[Type[DataFilter]]):
        """
        Initializes a FilterSequence object.

        Parameters:
        - data (DataFrame): The input DataFrame to be filtered.
        - filter_stack (list[Type[DataFilter]]): A list of DataFilter classes representing the sequence of filters to be applied.
        """
        self.data = data
        self.filter_stack = filter_stack


    def filter(self, *args, **kwargs):

        """
         Executes the filter sequence on the provided DataFrame
         Returns:
         - DataFrame: The filtered DataFrame.
         """
        result = self.data

        for data_filter in self.filter_stack:
            result = data_filter(result).filter()

        return result
