## Math libraries
# Data frames
import pandas as pd
# General array math library
import numpy as np
# Graph library
import matplotlib.pyplot as plt

## Toolbox classes
# Text manipulation
from Toolbox import Text as txt


class BoxPlot:
    def __init__(self):
        return

    def uniqueBoxplot(self, labels, values):
        plt.close()
        # Get the unique values
        unique = pd.unique(labels)
        # Get the data list
        data = []
        for label in unique:
            data.append(values[labels == label])
        # Add newlines where needed to labels
        for indx in range(len(unique)):
            unique[indx] = txt.Text().addSeperator(unique[indx], maxspace=30)
        # Store processed data.
        self.mLabels = unique
        self.mData = data
        return

    def draw(self, *, outlier=True, title=""):
        # Clear any previous figures
        plt.close()
        # Create new figure and axes
        fig, axes = plt.subplots()
        # Plot graph
        axes.set_title(title)
        bxPlot = axes.boxplot(x=self.mData, labels=self.mLabels, showfliers=outlier)
        # Rotate and change xtick labels size
        plt.xticks(rotation=90, fontsize=8)
        # Store the whiskers generator of the plot
        self.mWhiskers = (x.get_ydata()[1] for x in bxPlot["whiskers"])
        # Adjust boundary spacing of graph
        plt.tight_layout()
        # Add grid
        plt.grid()
        # Show graph
        # plt.show()
        return

    mLabels = None
    mData = None
    mWhiskers = None