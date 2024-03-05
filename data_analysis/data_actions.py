from abc import ABC

import pandas as pd
from pandas import DataFrame, Series


class DataAction(ABC):
    """
    Class to perform actions on data.
    """
    def run(self) -> DataFrame | Series:
        """
        run the specific action
        :return:
        """

