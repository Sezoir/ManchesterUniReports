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
            "boxSchoolManHours": None,
            "statistics": None
        }
        return

    # Creates the pdf file
    def createPDF(self):
        # Create section
        with self.mDoc.create(pyl.Section("School statistics:")) as sec1:
            # Add flavour text to section
            sec1.append("The following are the statistics of the manHours of each job according to school:")
            # Add long table of statistics to section
            self.addTable(sec1, self.mBank["statistics"], subxlabel={"#":["count"], "Hours":["mean", "lower quartile", "median", "upper quartile"]})

        # Create section
        with self.mDoc.create(pyl.Section("School against manHours")) as sec2:
            # Add flavour text to section
            sec2.append("These boxplots show the spread of the manHours for each school who have booked over 15 jobs.")
            # Add two boxplots to the section, where one shows the outliers and the other doesnt
            self.addGraph(sec2, "boxSchoolManHours", ylim=(0, 80), title="Schools against manHours with outliers")
            self.addGraph(sec2, "boxSchoolManHours", outlier=False, title="Schools against manHours without outliers")

        # Generate the pdf, and clean the latex files afterwards
        self.mDoc.generate_pdf(clean=True)
        return
