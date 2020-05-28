## Math libraries
# Data frames
import pandas as pd
# General array math library
import numpy as np

class Statistics:
    def __init__(self):
        return

    def getMean(self, data):
        if isinstance(data, pd.Series):
            return data.mean()
        return

    def getMedian(self, data):
        if isinstance(data, pd.Series):
            return data.median()
        return

    def getQuantile(self, data, quantile):
        if isinstance(data, pd.Series):
            return data.quantile(quantile)
        return

    def getGroupedStats(self, dataframe, groupColumn, statColumn):
        lowQuartile = lambda x: x.quantile(0.25)
        lowQuartile.__name__ = "lower quartile"
        uppQuartile = lambda x: x.quantile(0.75)
        uppQuartile.__name__ = "upper quartile"
        statistics = dataframe.groupby(groupColumn)[statColumn].agg(
            ["count", "mean", lowQuartile, "median", uppQuartile])
        return statistics