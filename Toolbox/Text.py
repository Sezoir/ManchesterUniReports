## Math libraries
# Data frames
import pandas as pd
# General array math library
import numpy as np

## Text libs
# Allows textwrap
import textwrap


class Text:
    def __init__(self):
        return

    # Add a "\n" after the maxspace limit for the inputted string or list of strings.
    # @todo add "inplace" option.
    def addSeperator(self, data, **options):
        if isinstance(data, str):
            return self.__Seperator__(data, **options)
        elif isinstance(data, list):
            lst = []
            for string in data:
                lst.append(self.__Seperator__(string, **options))
            return lst
        else:
            raise TypeError("Inputted data is of wrong type. Must be string of list of strings.")

    # Add a "\n" after the maxspace limit for the inputted string.
    # (Note that we use keywords here instead of **kwargs to catch errors if parameter is misspelled)
    def __Seperator__(self, data, *, maxspace=10):
        return textwrap.fill(data, width=maxspace, break_long_words=False)