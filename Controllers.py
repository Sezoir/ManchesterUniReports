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
        # Create ReportOne
        self.report(cntrOne.Controller)

        return

    def report(self, reportController):
        # Create the report
        report = reportController(self.mPres)
        # Create pdf report
        report.create()
        # Delete report class
        del report
        # Clear filter on Presenter
        self.mPres.clearFilters()
        return


    mPres = None