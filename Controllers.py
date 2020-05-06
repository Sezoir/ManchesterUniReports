## Math libraries
# Data frames
import pandas as pd
# General array math library
import numpy as np

## Controllers
import ReportOne.Controller as cntrOne


## Presenter
from Presenter import Presenter as pres


class Controllers:
    def __init__(self):
        # Create/store presenter
        self.mPres = pres.Presenter()
        # Create the first report
        report = cntrOne.Controller(self.mPres)
        # Create report
        report.create()
        # Clear filter and first report is done, ready for the next report
        self.mPres.clearFilters()

        return


    mPres = None