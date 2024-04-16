# Analysis and datatransformation tool
* transform your Data into a specific format
* convert from xlsx to csv
* analyze your data

## Components
1. `Analyzer`: responsibility to orchestrate other components and set up filters etc
2. `DataLoader`: responsibility to load the data, format and preprocess it
3. `Plotter`: responsibility to make Plots 
4. `DataFilter`: responsibility to filter the preprocessed data
5. `FilterSequence`: chain together multiple DataFilter

### 1. Analyzer
Requires a configuration Dictionary and an [DataLoader](#2-dataloader) instance:
```python
CONFIG = {
    "file_path": "path/to/your/data",   # either a directory or a file
    "data_out_path": "path/where/you/want/the/processed/data",  # must be dir
    "plot_path": "path/where/you/want/the/plot/images", # must be dir
    "drop_cols": ["Typ", "Label Obj. Moralwerte", "Label Subj. Moralwerte", "Label Kommunikative Funktionen",
                  "Spans Kommunikative Funktionen", "Label Protagonist:innen", "Spans Protagonist:innen",
                  "Label Explizite Forderungen", "Spans Explizite Forderung", "Label Implizite Forderungen",
                  "Spans Implizite Forderung"], # the columns that should be dropped on preprocessing; this is the default
    "merge_cols": ["Spans Obj. Moralwerte", "Spans Subj. Moralwerte"],  # columns that should be merged on preprocessing; this is the default
}

```
* `.occurrences_to_csv()`: use this to process the raw xlsx to csvs. Returns the preprocessed DataFrames. If `aggregate` is set to `False` (default), spans that occure multiple times won't be merged, so you can analyze every instance of that span.
* `.make_piecharts()`: makes a pie-chart of the moral value distribution accross the list of DataFrames passed to `data_que`. Change the style by passing a [color map](https://matplotlib.org/stable/gallery/color/colormap_reference.html) string to `c_map` (Default: `"tab20b"`). Expects a [DataFilter or DataFilterSequence](#4-datafilter) passed to `data_filter`.
* `.plot_phrases()`: makes a pie-chart showing the percentage of annotated moral values to each phrase in the given DataFrame. Same options as in `make_piecharts()`
* `.make_bar_chart()`: makes a bar chart plotting annotated moral values by dynamic categories (as passed in `data_dict`).
    The data is normalized in comparison to the whole data by default, this can be toggled of by passing `normalize=False`.
    If a valid path is passed to `save_path`, the plot will be saved to that path, otherwise the figure will only be shown. If `inverted` is set to `True`, the plot will have the moral values on the x-axis and the bars representing the categories. The kwarg `divide_by_anno` can be set to `False` in order to normalize the data by dividing through the len of the num of paragraphs in one category. By Default it is set to `True`, meaning normalization is achieved by dividing through the total sum of annotated values within a category.
### 2. DataLoader
Requires a Config Dictionary (like [Analyzer](#1-analyzer)). Best instantiated by calling the `get_loader()` method since it will choose between `FileDataLoader` and `DirDataLoader`:
```Python
data_loader = DataLoader.get_loader(CONFIG)
```

### 3. Plotter
Will be instantiated on initializing the [Analyzer](#1-analyzer) class. Control what should be plotted by using [DataFilters](#4-datafilter) or a [FilterSequence](#5-filtersequence)

### 4. DataFilter
Parent to multiple DataFilter classes to filter and transform Data und specific criteria. Has some utility classes.
Eg.:
* `MoralDistributionFilter`: filters out the "phrases" column and adds up all moral values
* `PhraseCrossOverFilter`: filters for phrases that have more than one moral value assigned to them
* `RegExFilter`: filters spans for hits on a RegularExpression (can be passed to **kwargs)
* `ConcatMultipleDataFrames`: utility Filter for concatenating multiple DataFrames to one

### 5. FilterSequence
Used to chain multiple Filters together. Do so by passing a list of classes (!not instances!) of [DataFilters](#4-datafilter) you want to use to `filter_stack`. Also expects a list of DataFrames to be passed to `data`.
Filter the data by calling the `filter()` method:
````python
seq = FilterSequence(dfs, [ConcatMultipleDataFrames, RegExFilter])

    outp = seq.filter(r_pattern=r_pat)
````



