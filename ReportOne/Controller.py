# Json lib
import json as json

## Math libraries
# Data frames
import pandas as pd
# General array math library
import numpy as np
# Graph library
import matplotlib.pyplot as plt

## Presenter
from Presenter import Presenter as pres

## Toolbox
# To create boxplot figures
import Toolbox.BoxPlot as bxplt
# Get general statistics and filtering
from Toolbox import Statistics, Filtering

## View class
from ReportOne import View as vw

##@todo:delete
import pylatex as pyl



class Controller:
    def __init__(self, pres):
        # Store presenter @todo: maybe remove variable and just store table
        self.mPres = pres
        # Add filters (we use greater than filter as ew assume that no job takes less than 1 hour to complete)
        self.mPres.addFilters({"Equals": [["internal", True]],
                               "GreaterThan": [["manHours", 0]]}) #"Date": [["createdAt", "2010-12-14", "2018-5-6"]],, ["standardjobtype", True]

        # Read json config file
        with open("ReportOne/config.json") as f:
            self.mConfig = json.load(f)

        # Get/store table, with selected columns
        # We use fuzzy to standardise the school names (for example all of chemistry comes
        # under "Department of Chemistry")
        self.mTable = self.mPres.getTable(["school", "manHours"], fuzzy=self.mConfig["school"])
        return

    def create(self):
        # Drop all jobs where man hours are N/A @todo: maybe include this in the Presenter class as an option
        self.mTable.dropna(axis=0, subset=["manHours"], inplace=True)

        # Get mean, lower quartile, median, upper quartile
        stats = Statistics.Statistics()
        statistics = stats.getGroupedStats(self.mTable, "school", "manHours")

        # Filter out all schools with less than 15 jobs total (to stop clutter of school, where there is not enough
        # information to show on graph.
        filt = Filtering.Filtering()
        filt.cntDrop(self.mTable, "school", 15)

        # Create boxplot class, and pass in columns/categories for plotting
        plot = bxplt.BoxPlot()
        plot.uniqueBoxplot(self.mTable.school, self.mTable.manHours)

        # Create view
        view = vw.View()
        # Update view class config
        view.updateBank({
            "table": self.mConfig["table"],
            "boxSchoolManHours": plot,
            "statistics": statistics})
        # Create pdf
        view.createPDF()
        return

    mTable = None
    mPres = None
    mConfig = None