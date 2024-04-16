from typing import Type, List

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import matplotlib as mpl
from pandas import Series, DataFrame

from data_analysis.data_filter import DataFilter, MoralDistributionFilter
from data_analysis.filter_sequence import FilterSequence


class Plotter:

    def __init__(self, config):
        self.config = config

    def _series_to_piechart(self, data: Series, c_map, save: bool = True):
        # config colors
        cmap = mpl.colormaps[c_map]
        colors = cmap(np.linspace(0, 1, len(data)))
        # init figure
        plt.figure(figsize=(11, 11))
        autopct_format = lambda p: f'{p:.1f}%\n{int(p * data.sum() / 100)}'
        plt.pie(data, labels=None, autopct=autopct_format, startangle=140, colors=colors)
        # Create a legend
        plt.legend(data.index, loc="best")
        if save:
            plt.savefig(self.config['plot_path'])
        else:
            plt.show()

    def plot_phrases(self, data_que: List[DataFrame], data_filter: Type[DataFilter | FilterSequence],
                     c_map: str = 'tab20b', save: bool = True):
        processed_data = None
        # process data
        for data in data_que:
            if processed_data is None:
                processed_data = self._preprocess_piechart(data, data_filter)
            else:
                new_data = self._preprocess_piechart(data, data_filter)
                processed_data = pd.concat([processed_data, new_data], axis=0)
        result_df = processed_data.groupby('phrase').sum().reset_index()

        as_list = self._dataframe_to_series(result_df)
        for srs in as_list:
            phrase = srs['phrase']
            print(f'processing: {phrase}')
            # init figure
            non_zero_indices = srs.values[1:] != 0
            labels = srs.index[1:][non_zero_indices]
            values = srs.values[1:][non_zero_indices]  # Exclude the first element, which is the phrase
            plt.figure()
            plt.pie(values, labels=labels, autopct=lambda p: f'{p:.2f}%\n({int(p * sum(values) / 100)})', startangle=90)
            plt.title(f'Moral Values Distribution for: "{phrase}"\nannotated values in total: {values.sum()}')
            if save:
                plt.savefig(f"imgs/{phrase}.png")
            else:
                plt.show()

    def _preprocess_piechart(self, data: DataFrame,
                             data_filter: Type[DataFilter | FilterSequence]) -> Series | DataFrame:
        """
        Helper method to preprocess data for pie chart
        :param data: DataFrame
        :return: DataFrame
        """
        # init filter
        cf = data_filter(data)
        # filter data
        processed_data = cf.filter()
        return processed_data

    def make_pie_chart(self, data: DataFrame, c_map: str = 'tab20b', save: bool = True) -> None:
        """
        Method to create pie chart of moral values by language
        :param data: DataFrame
        :return: None
        """
        # process data
        processed_data = self._preprocess_piechart(data, MoralDistributionFilter)
        self._series_to_piechart(processed_data, c_map, save=save)

    def make_pie_charts(self, data_que: List[DataFrame], data_filter: Type[DataFilter | FilterSequence],
                        c_map: str = 'tab20b', save: bool = True) -> None:
        """
        Method to create pie chart
        :param data_filter: DataFilter or FilterSequence
        :param data_que: list of Dataframes to be processed
        :return: None
        """
        processed_data = None
        # process data
        for data in data_que:
            if processed_data is None:
                processed_data = self._preprocess_piechart(data, data_filter)
            else:
                processed_data += self._preprocess_piechart(data, data_filter)

        self._series_to_piechart(processed_data, c_map, save=save)

    def make_bar_chart(self, data_dict: dict, save_path: str, normalize: bool = True):
        categories = list(data_dict.keys())
        moral_values = data_dict[categories[0]][2].index.tolist()  # Assuming all categories have the same moral values
        num_categories = len(categories)
        bar_width = 0.1
        index = np.arange(len(moral_values))

        plt.figure(figsize=(16, 8))  # Increased figure size
        if normalize:
            for i, category in enumerate(categories):
                normalization_factor = data_dict[category][1]
                values = data_dict[category][2] * normalization_factor
                plt.bar(index + i * bar_width, values, bar_width,
                        label=f"{category}: {round(normalization_factor * 100, 2)}%")
        else:
            for i, category in enumerate(categories):
                values = data_dict[category][2]
                plt.bar(index + i * bar_width, values, bar_width, label=f"{category}: {data_dict[category][0]}")

        plt.xlabel('Moral Values')
        plt.ylabel('Count')
        plt.title(f'Moral Values Distribution by Category (normalized: {normalize})')
        plt.xticks(index + bar_width * (num_categories - 1) / 2, moral_values)
        plt.legend()
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()

    def _dataframe_to_series(self, data: DataFrame) -> List[Series]:
        list_of_series = [pd.Series(row[1]) for row in data.iterrows()]
        return list_of_series


if __name__ == "__main__":
    pass
