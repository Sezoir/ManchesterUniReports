## Base class
import ViewBase as vwbs

## Toolbox
# To store boxplot figures
import Toolbox.BoxPlot as bxplt

## PDF creator
import pylatex as pyl

# Graph library
import matplotlib.pyplot as plt


class View(vwbs.ViewBase):
    def __init__(self):
        super().__init__("ReportOne")
        self.mBank = {
            "boxSchoolManHours": None
        }
        print("Done")
        return

    def createPDF(self):
        self.mDoc.append('Introduction.')

        with self.mDoc.create(pyl.Section('I am a section')):
            self.mDoc.append('Take a look at this beautiful plot:')

            self.addGraph(self.mDoc, "boxSchoolManHours", ylim=(0,80),title="Schools against manHours with outliers")
            self.addGraph(self.mDoc, "boxSchoolManHours", outlier=False, title="Schools against manHours without outliers")
            self.mDoc.append('Created using matplotlib.')

        self.mDoc.append('Conclusion.')

        self.mDoc.generate_pdf(clean=True)
        return
