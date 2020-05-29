## Import project classes for testing
from Repository import Repository as repo
from Presenter import Presenter as pres
from Presenter import Equals as propFil
import Controllers as contr

## Record time
import time as time

## Record memory usage
import tracemalloc

## Math libraries
# Data frames
import pandas as pd
# General array math library
import numpy as np

def usage(func):
    tracemalloc.start()
    t = time.time()
    fun = func()
    elapsed = time.time() - t
    print(f"Time elapsed is {elapsed} seconds")
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
    tracemalloc.stop()
    return fun

def main():
    # Set properties of console for pandas
    desired_width = 320
    pd.set_option('display.width', desired_width)
    pd.set_option('display.max_columns', 5)

    # Test reports
    cons = usage(contr.Controllers)

    # Test Presenter class with filters
    # prest = pres.Presenter()
    # prest.addFilters({"Equals": [["internal", True], ["standardjobtype", True]]})
    # prest.addFilters({"Date": [["createdAt", "2016-1-1", "2018-5-6"]]})
    # prest.addFilters({"Equals": [["internal", True], ["standardjobtype", True]],
    #                   "Date": [["createdAt", "2016-1-1", "2018-5-6"]]})
    # print(prest.getTable(["school", "manHours"]))

    return

if __name__ == "__main__":
    main()
