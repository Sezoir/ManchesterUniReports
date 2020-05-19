## PDF creator
import pylatex as pyl

## Graph library
import matplotlib.pyplot as plt

# Base class for any View class made in a report
class ViewBase:
    def __init__(self, path):
        # Declare data bank as empty dict
        self.mBank = {}
        # Set geometry options
        geometry_options = {"right": "2cm", "left": "2cm"}
        # Create document
        self.mDoc = pyl.Document(geometry_options=geometry_options, default_filepath=path+"/report")
        return

    # Update the bank with data to be used for pdf creation
    def updateBank(self, data):
        # Update dict
        self.mBank.update(data)
        return

    # Add a graph to the document
    # @todo: change to allow flexible pylatex parameters (probably using dict)
    def addGraph(self, doc, plotName, *, ylim=(), **graphOptions):
        # Attempt to create figure
        with doc.create(pyl.Figure(position='htbp')) as plot:
            # Plot graph
            self.mBank[plotName].draw(**graphOptions)
            # Matplotlib axes options
            if ylim != ():
                plt.ylim(ylim)
            # Add plot to document
            plot.add_plot(width=pyl.NoEscape(r'1\textwidth'), dpi=300)
        return

    # A data bank, which stores reference to data results to be shown from the Controller
    mBank = None
    # Reference to document
    mDoc = None
