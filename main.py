from Repository import Repository as repo
from Presenter import Presenter as pres
from Presenter import Equals as propFil
import Controllers as contr

import time as time

import tracemalloc

import Backup.RepositoryOld as repo2

## Math libraries
# Data frames
import pandas as pd
# General array math library
import numpy as np

def main():
    # Test reports
    cons = contr.Controllers()

    # Test Presenter class with filters
    # prest = pres.Presenter()
    # prest.addFilters({"Equals": [["internal", True], ["standardjobtype", True]]})
    # prest.addFilters({"Date": [["created_at", "2016-1-1", "2018-5-6"]]})
    # prest.addFilters({"Equals": [["internal", True], ["standardjobtype", True]],
    #                   "Date": [["created_at", "2016-1-1", "2018-5-6"]]})
    # print(prest.getTable(["school", "man_hours"]))

    # Test speed of Repository class
    # t = time.time()
    # re = repo.Repository()
    # elapsed = time.time() - t
    # print(elapsed)
    # print(re.mJobs)

    # tracemalloc.start()
    # t = time.time()
    # re = repo.Repository()
    # print(re.mJobs[re.mJobs.man_hours == 0])
    # elapsed = time.time() - t
    # print(elapsed)
    # print(re.mJobs)
    # current, peak = tracemalloc.get_traced_memory()
    # print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
    # tracemalloc.stop()
    #
    # del re

    # tracemalloc.start()
    # t = time.time()
    # re = repo2.Repository()
    # elapsed = time.time() - t
    # print(elapsed)
    # print(re.mJobs)
    # current, peak = tracemalloc.get_traced_memory()
    # print(f"Current memory usage is {current / 10 ** 6}MB; Peak was {peak / 10 ** 6}MB")
    # tracemalloc.stop()


    return

if __name__ == "__main__":
    main()
