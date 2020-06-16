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
            "graphs": [],
            "statistics": [],
            "dateBegin": [],
            "dateEnd": [],
            "type": []
        }
        return

    # Creates the pdf file
    def createPDF(self):
        # Loop through each pacakage
        for ind in range(len(self.mBank["dateEnd"])):
            # Generate type of text to be used for report
            text = self.genText(ind)
            # Create section
            with self.mDoc.create(pyl.Section(self.mBank["dateBegin"][ind]+" - " + self.mBank["dateEnd"][ind])) as sec:
                # Add description of table
                sec.append(text["description"])
                # Add long table of statistics to section
                self.addTable(sec, self.mBank["statistics"][ind], subxlabel={"#":["count"], "Hours":["mean", "lower quartile", "median", "upper quartile"]})
                self.addGraph(sec, self.mBank["graphs"][ind], title=text["plotTitle"])
            # Append new page after table/graph
            self.mDoc.append(pyl.NewPage())

        # Generate the pdf, and clean the latex files afterwards
        self.mDoc.generate_pdf(clean=True)
        return

    def genText(self, ind):
        text = {}
        if self.mBank["type"][ind] == "jobs":
            text["description"] = "A table showing statistics of all jobs created between " + self.mBank["dateBegin"][ind]+" - "+self.mBank["dateEnd"][ind] + " arranged per school."
            text["plotTitle"] = "Schools against manHours"
        elif self.mBank["type"][ind] == "jobsType":
            text["description"] = "A table showing statistics of all jobs created between " + self.mBank["dateBegin"][ind] + " - " + self.mBank["dateEnd"][ind] + " arranged per job type."
            text["plotTitle"] = "Job types against manHours"
        return text
