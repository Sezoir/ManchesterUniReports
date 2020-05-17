## Toolbox
# To store boxplot figures
import Toolbox.BoxPlot as bxplt

## PDF creator
import pylatex as pyl


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

            with doc.create(pyl.Figure(position='htbp')) as plot:
                self.mPlots["boxSchoolManHours"].draw()
                plot.add_plot(width=pyl.NoEscape(r'1\textwidth'), dpi=300)
                plot.add_caption('I am a caption.')

            doc.append('Created using matplotlib.')

        doc.append('Conclusion.')

        doc.generate_pdf(clean=True)
        return

    mPlots = None
