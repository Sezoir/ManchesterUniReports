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
        geometry_options = \
            {
                "landscape": True,
                "right": "2cm",
                "left": "2cm"
            }
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
    def addTable(self, doc, dataframe, *, xlabel="", ylabel="", subxlabel={}):
        # Limit decimal places being too long
        # @todo: find way without copying
        dataframe = dataframe.round(2)
        # Count columns (including index)
        clnCount = len(dataframe.columns)+1
        # Create long table (note we want string as longtable parameter in form "l l l ..." for each column)
        with doc.create(pyl.LongTable(" ".join(["l" for x in range(clnCount)]))) as table:
            # Get order of columns
            order = [dataframe.index.name] + list(dataframe.columns)
            # Check whether to add subcolumn grouping
            if subxlabel != {}:
                order = self.subColumn(table, order, subxlabel)
            # Add the column names row
            table.add_hline()
            table.add_row(order, color="DarkGray")
            table.add_hline()
            # Insert the data row by row
            for ind in range(len(dataframe)):
                # Add alternating color to each row
                if ind%2 == 0:
                    table.add_row(self.getRow(dataframe, ind, order=order))
                else:
                    table.add_row(self.getRow(dataframe, ind, order=order), color="LightGray")
        return

    # Adds a "subcolumn" row to the table to group columns together, e.g: "Hours"
    def subColumn(self, table, columns, subcolumns):
        # Create list of unlabelled columns
        unlabelled = [z for z in columns if z not in [x for x in columns for y in subcolumns.values() if x in y]]
        # Track order of the columns
        order = []
        order += unlabelled
        order += [y for x in subcolumns.values() for y in x]
        # Add hline
        # table.add_hline()
        # Create empty list for storing the multicolumns
        multiCol = []
        # Add multicolumn for the index and columns with no sublabel
        # Non-sublabelled columns/index
        for x in unlabelled:
            multiCol.append(pyl.MultiColumn(1, align="c", data=""))
        # Add multicolumn now for each subcolumn
        for key in subcolumns:
            multiCol.append(pyl.MultiColumn(len(subcolumns[key]), align="|c|", data=key, color="DarkGray"))
        # Append subcolumns row to table
        table.add_row(multiCol)
        return order

    def getRow(self, dataframe, index, order):
        row = [dataframe.index[index]]
        for column in order[1:]:
            row.append(dataframe.iloc[index, dataframe.columns.get_loc(column)])
        return row

    # A data bank, which stores reference to data results to be shown from the Controller
    mBank = None
    # Reference to document
    mDoc = None
