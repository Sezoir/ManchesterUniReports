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
        uniqueSchools = pd.unique(self.mTable.school)
        cnt = self.mTable["school"].value_counts().to_dict()
        # Drop all schools with less than 15 jobs (stops clutter of schools, where there is not enough information)
        for school in uniqueSchools:
            if cnt[school] < 15:
                self.mTable.drop(index=self.mTable.index[self.mTable.school == school], axis=0, inplace=True)

        # Drop all jobs where man hours are N/A @todo: maybe include this in the Presenter class as an option
        self.mTable.dropna(axis=0, subset=["manHours"], inplace=True)

        axes = self.mTable.boxplot(column=["manHours"], by="school",rot=10,return_type="axes")
        # plt.show()

        print(self.mTable)
        # print(self.mTable.manHours[self.mTable.school == "Department Of Chemistry"])
        # for i, g in self.mTable.groupby("school"):
        #     print(i,g)

        test = bxplt.BoxPlot()
        test.uniqueBoxplot(self.mTable.school, self.mTable.manHours)
        test.draw()

        test2 = bxplt.BoxPlot()
        test2.uniqueBoxplot(self.mTable.school, self.mTable.manHours)
        test2.draw()

        test.draw()

        geometry_options = {"right": "2cm", "left": "2cm"}
        doc = pyl.Document(geometry_options=geometry_options, default_filepath="ReportOne/test")

        doc.append('Introduction.')

        with doc.create(pyl.Section('I am a section')):
            doc.append('Take a look at this beautiful plot:')

            with doc.create(pyl.Figure(position='htbp')) as plot:
                plot.add_plot(width=pyl.NoEscape(r'1\textwidth'), dpi=300)
                plot.add_caption('I am a caption.')

            doc.append('Created using matplotlib.')

        doc.append('Conclusion.')

        doc.generate_pdf(clean=True)


        return

    mTable = None
    mPres = None