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


class Controller:
    def __init__(self, pres):
        # Store presenter @todo: maybe remove variable and just store table
        self.mPres = pres
        # Add filters (we use greater than filter as ew assume that no job takes less than 1 hour to complete)
        self.mPres.addFilters({"Equals": [["internal", True], ["standardjobtype", True]],
                               "Date": [["createdAt", "2016-1-1", "2018-5-6"]],
                               "GreaterThan": [["manHours", 0]]})
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
        uniqueSchools = pd.unique(self.mTable.school)
        cnt = self.mTable["school"].value_counts().to_dict()
        print(type(cnt))
        print(cnt)
        print(cnt["Department Of Chemistry"])
        # Drop all schools with less than 15 jobs (stops clutter of schools, where there is not enough information)
        for school in uniqueSchools:
            if cnt[school] < 15:
                self.mTable.drop(index=self.mTable.index[self.mTable.school == school], axis=0, inplace=True)

        # Drop all jobs where man hours are N/A @todo: maybe include this in the Presenter class as an option
        self.mTable.dropna(axis=0, subset=["manHours"], inplace=True)

        print(uniqueSchools)
        self.mTable.boxplot(column=["manHours"], by="school")
        plt.show()
        return

    mTable = None
    mPres = None