## Base class
import ViewBase as vwbs

## Toolbox
# To store boxplot figures
import Toolbox.BoxPlot as bxplt

## PDF creator
import pylatex as pyl

## Pylatex external packages support
import LaTeX.Lscape as pyle

# Graph library
import matplotlib.pyplot as plt


class View(vwbs.ViewBase):
    def __init__(self):
        # Set init parameters of parent class
        super().__init__("ReportOne")
        # Initialise data bank
        self.mBank = {
            "graphs": None,
            "statistics": None,
            "dateBegin": [],
            "dateEnd": []
        }
        return

    # Creates the pdf file
    def createPDF(self):
        # Loop through each pacakage
        for ind in range(len(self.mBank["dateEnd"])):
            # Create section
            with self.mDoc.create(pyl.Section(self.mBank["dateBegin"][ind]+" - "+self.mBank["dateEnd"][ind])) as sec:
                # Add long table of statistics to section
                self.addTable(sec, self.mBank["statistics"][ind], subxlabel={"#":["count"], "Hours":["mean", "lower quartile", "median", "upper quartile"]})
                self.addGraph(sec, self.mBank["graphs"][ind], ylim=(0, 80), title="Schools against manHours")
            # Append new page after table/graph
            self.mDoc.append(pyl.NewPage())

        # Generate the pdf, and clean the latex files afterwards
        self.mDoc.generate_pdf(clean=True)
        return
