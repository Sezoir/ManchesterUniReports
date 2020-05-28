## Math libraries
# Data frames
import pandas as pd
# General array math library
import numpy as np

class Filtering:
    def __init__(self):
        return

    def cntDrop(self, dataframe, column, min):
        # Get all unique keys
        uniqueKeys = pd.unique(dataframe[column])
        cnt = dataframe[column].value_counts().to_dict()
        # Drop all keys with less than minimum count
        for key in uniqueKeys:
            if cnt[key] < min:
                dataframe.drop(index=dataframe.index[dataframe[column] == key], axis=0, inplace=True)
        return