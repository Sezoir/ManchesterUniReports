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
            config = json.load(f)

        # Get/store table, with selected columns
        # We use fuzzy to standardise the school names (for example all of chemistry comes
        # under "Department of Chemistry")
        self.mTable = self.mPres.getTable(["school", "manHours"], fuzzy=config)
        # print(self.mTable)
        return

    def create(self):
        # Get all unique school names
        uniqueSchools = pd.unique(self.mTable.school)
        cnt = self.mTable["school"].value_counts().to_dict()
        # Drop all schools with less than 15 jobs (stops clutter of schools, where there is not enough information)
        for school in uniqueSchools:
            if cnt[school] < 15:
                self.mTable.drop(index=self.mTable.index[self.mTable.school == school], axis=0, inplace=True)

        # Drop all jobs where man hours are N/A @todo: maybe include this in the Presenter class as an option
        self.mTable.dropna(axis=0, subset=["manHours"], inplace=True)

        print(self.mTable)

        # Create boxplot class, and pass in columns/categories for plotting
        plot = bxplt.BoxPlot()
        plot.uniqueBoxplot(self.mTable.school, self.mTable.manHours)

        # Get mean, lower quartile, median, upper quartile
        # Create lower/upper lambda funcs
        lowQuartile = lambda x: x.quantile(0.25)
        lowQuartile.__name__ = "lower quartile"
        uppQuartile = lambda x: x.quantile(0.75)
        uppQuartile.__name__ = "upper quartile"
        statistics = self.mTable.groupby("school")["manHours"].agg(["mean", lowQuartile, "median", uppQuartile])
        print(statistics)

        # Create view
        view = vw.View()
        # Update view class with statistical results
        view.updateBank({"boxSchoolManHours": plot,
                          "statistics": statistics})
        # Create pdf
        view.createPDF()
        return

    mTable = None
    mPres = None