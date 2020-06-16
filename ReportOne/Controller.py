## Python libs
# Json lib
import json as json
# Date lib
import datetime as dt
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

# CntDrop filter (as we want to filter after we have got a "fuzzy" table)
from Presenter import CntDrop as filt

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

        # View config
        vConfig = {
            "statistics": [],
            "graphs": [],
            "dateBegin": [],
            "dateEnd": [],
            "type": []
        }
        # Loop through each date
        for package in self.mConfig["data"]:
            # Get the dateBegin and dateEnd
            dateBegin = ""
            dateEnd = ""
            # Check whether key exists/open-ended
            if ("dateBegin" not in package) or package["dateBegin"] == "":
                # Use minimum date in dataframe
                dateBegin = self.mTable.createdAt.min().date().strftime("%d/%m/%Y")
            else:
                dateBegin = package["dateBegin"]
            # Check whether key exists/open-ended
            if ("dateEnd" not in package) or package["dateEnd"] == "":
                # Use current date
                dateEnd = dt.date.today().strftime("%d/%m/%Y")
            else:
                dateEnd = package["dateEnd"]
            # Append dates to vConfig
            vConfig["dateBegin"].append(dateBegin)
            vConfig["dateEnd"].append(dateEnd)

            # Create report depending on type in config
            if package["type"] == "jobs":
                self.jobsReport(vConfig, dateBegin, dateEnd, package["minimumCount"])
            elif package["type"] == "jobsType":
                self.jobsTypeReport(vConfig, dateBegin, dateEnd, package["minimumCount"])

            # Store type of report created
            vConfig["type"].append(package["type"])

        # Create view
        view = vw.View()
        # Update view class config
        view.updateBank(vConfig)
        # Create pdf
        view.createPDF()
        return

    def jobsReport(self, config, dateBegin, dateEnd, minimumCount):
        # Get table within date period from config
        self.mPres.clearFilters()
        self.mPres.addFilters({"Equals": [["internal", True]],
                               "GreaterThan": [["manHours", 0]],
                               "Date": [["createdAt", dateBegin, dateEnd]]})
        self.mTable = self.mPres.getTable(["school", "manHours", "createdAt"], fuzzy=self.mConfig["school"])

        # Get mean, lower quartile, median, upper quartile
        stats = Statistics.Statistics()
        config["statistics"].append(stats.getGroupedStats(self.mTable, "school", "manHours"))

        # Filter out all schools with less than x jobs total (to stop clutter of school, where there is not enough
        # information to show on graph.
        filter = filt.CntDrop(["school", minimumCount])
        reducedTable = self.mTable.loc[filter.filter(self.mTable), :]

        # Create boxplot class, and pass in columns/categories for plotting
        plot = bxplt.BoxPlot()
        plot.uniqueBoxplot(reducedTable.school, reducedTable.manHours)
        config["graphs"].append(plot)
        return

    def jobsTypeReport(self, config, dateBegin, dateEnd, minimumCount):
        # Get table within date period from config
        self.mPres.clearFilters()
        self.mPres.addFilters({"Equals": [["internal", True]],
                               "GreaterThan": [["manHours", 0]],
                               "Date": [["createdAt", dateBegin, dateEnd]]})
        self.mTable = self.mPres.getTable(["jobType", "manHours"], fuzzy=self.mConfig["school"])

        # Get mean, lower quartile, median, upper quartile
        stats = Statistics.Statistics()
        config["statistics"].append(stats.getGroupedStats(self.mTable, "jobType", "manHours"))

        # Create boxplot class, and pass in columns/categories for plotting
        plot = bxplt.BoxPlot()
        plot.uniqueBoxplot(self.mTable.jobType, self.mTable.manHours)
        config["graphs"].append(plot)
        return

    mTable = None
    mPres = None
    mConfig = None