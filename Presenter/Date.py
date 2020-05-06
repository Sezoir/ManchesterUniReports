## Math libraries
# Data frames
import pandas as pd
# Pandas errors
from pandas.errors import ParserError
# General array math library
import numpy as np

class Date:

    def __init__(self, parameterPack):
        self.mKey = parameterPack[0]
        self.mStartDate = parameterPack[1]
        self.mEndDate = parameterPack[2]

        return
    def filter(self, table):
        # Ensure column is a pandas series of datetime64 dtype
        try:
            table.update(pd.to_datetime(table[self.mKey]))
        except Exception as e:
            print("Cannot convert to datetime in class Date: ", e.args[0])

        # table.loc[:, self.mKey] = pd.to_datetime(table[self.mKey])
        # Create column of true booleans
        mask = [True for x in table.index]
        # Check whether to use a start date
        if self.mStartDate != "":
            # Update mask of all dates greater than start date
            mask = mask & (table[self.mKey] > self.mStartDate)
        # Check whether to use a end date
        if self.mEndDate != "":
            # Update mask of all dates less than end date
            mask = mask & (table[self.mKey] < self.mEndDate)
        # Apply mask and drop all NaT values
        # table.drop(table[~mask].index, axis=0, inplace=True)
        return mask

    mKey = None
    mStartDate = None
    mEndDate = None