## Toolbox
# To store boxplot figures
import Toolbox.BoxPlot as bxplt

## PDF creator
import pylatex as pyl

# Graph library
import matplotlib.pyplot as plt


class View:
    def __init__(self):
        self.mPlots = {
            "boxSchoolManHours": None
        }
        return

    def updatePlots(self, plotDict):
        self.mPlots.update(plotDict)
        return

    def createPDF(self):
        geometry_options = {"right": "2cm", "left": "2cm"}
        doc = pyl.Document(geometry_options=geometry_options, default_filepath="ReportOne/test")

        doc.append('Introduction.')

        with doc.create(pyl.Section('I am a section')):
            doc.append('Take a look at this beautiful plot:')

            self.addGraph(doc, "boxSchoolManHours", ylim=(0,80),title="Schools against manHours with outliers")
            self.addGraph(doc, "boxSchoolManHours", outlier=False, title="Schools against manHours without outliers")
            doc.append('Created using matplotlib.')

        doc.append('Conclusion.')

        doc.generate_pdf(clean=True)
        return

    # Add a graph to the document
    # @todo: change to allow flexible pylatex parameters (probably using dict)
    def addGraph(self, doc, plotName, *, ylim=(), **graphOptions):
        # Attempt to create figure
        with doc.create(pyl.Figure(position='htbp')) as plot:
            # Plot graph
            self.mPlots[plotName].draw(**graphOptions)
            # Matplotlib axes options
            if ylim != ():
                plt.ylim(ylim)
            # Add plot to document
            plot.add_plot(width=pyl.NoEscape(r'1\textwidth'), dpi=300)
        return

    mPlots = None
