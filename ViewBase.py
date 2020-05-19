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
        # Declare packages
        self.mDoc.add_color("LightGray", "rgb", "0.83, 0.83, 0.83")
        self.mDoc.add_color("DarkGray", "rgb", "0.66, 0.66, 0.66")
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

    # Takes a dataframe and adds a multirow table to the document
    def addTable(self, doc, dataframe, *, xlabel="", ylabel=""):
        # Limit decimal places being too long
        # @todo: find way without copying
        dataframe = dataframe.round(2)
        # Count columns (including index)
        clnCount = len(dataframe.columns)+1
        # Create long table (note we want string as longtable parameter in form "l l l ..." for each column)
        with doc.create(pyl.LongTable(" ".join(["l" for x in range(clnCount)]))) as table:
            table.add_hline()
            table.add_row([dataframe.index.name] + list(dataframe.columns), color="DarkGray")
            table.add_hline()
            for ind in range(len(dataframe)):
                # Add alternating color to each row
                if ind%2 == 0:
                    table.add_row([dataframe.index[ind]] + list(dataframe.iloc[ind]))
                else:
                    table.add_row([dataframe.index[ind]] + list(dataframe.iloc[ind]), color="LightGray")
            # for ind in dataframe.index:
            #     table.add_row([ind] + list(dataframe.loc[ind]))
        return

    # A data bank, which stores reference to data results to be shown from the Controller
    mBank = None
    # Reference to document
    mDoc = None
