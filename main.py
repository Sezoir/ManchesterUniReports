from Repository import Repository as repo
from Backup import RepositoryNew as repo2
from Presenter import Presenter as pres
from Presenter import Equals as propFil

import Controllers as contr

## Math libraries
# Data frames
import pandas as pd
# General array math library
import numpy as np

def main():
    cons = contr.Controllers()

    # prest = pres.Presenter()
    # prest.addFilters({"Equals": [["internal", True], ["standardjobtype", True]]})
    # prest.addFilters({"Date": [["created_at", "2016-1-1", "2018-5-6"]]})
    # prest.addFilters({"Equals": [["internal", True], ["standardjobtype", True]],
    #                   "Date": [["created_at", "2016-1-1", "2018-5-6"]]})
    # print(prest.getTable(["school", "man_hours"]))
    # t = time.time()
    # re = repo.Repository()
    # elapsed1 = time.time() - t
    # t = time.time()
    # re2 = repo2.Repository()
    # elapsed2 = time.time() - t
    # print(elapsed1,elapsed2)
    return

if __name__ == "__main__":
    main()
