## Math libraries
# Data frames
import pandas as pd
# General array math library
import numpy as np

import importlib

## Repository
from Repository import Repository as repo


class Presenter:
    # Initialise class by getting repo table, formatting column names, and setting mask on mFilTable.
    def __init__(self):
        # Create instance of repo
        self._mRepo = repo.Repository()
        # Store table
        self._mTable = self._mRepo.mJobs
        # Initialise the mask
        self._mFilTable = [True for x in range(len(self._mTable.index))]
        # Rename columns
        self._renameColumns()

        # Quick test @todo: delete test later
        print(self._mTable.columns)
        # @todo: First remove any "test" data from table
        return

    # Takes a dictionary of filters, and creates a mask based on the filter. Mask is stored as _mFilTable.
    def addFilters(self, filters):
        # Iterate through each filter
        for filter in filters:
            # Import the associated file based on the filter
            module = importlib.import_module("."+filter, package=__package__)
            # Get a instance of the class from the imported file
            class_ = getattr(module, filter)
            # Iterate through each instance for the current filter (in case we want to apply the same filter multiple
            # times.
            for instance in filters[filter]:
                # Create the class with parameter keys based on the current instance
                filterClass = class_(instance)
                # Get the mask from the filterClass and simply AND check against stored mask
                self._mFilTable = self._mFilTable & filterClass.filter(self._mTable)
        return

    # Resets the stored mask.
    def clearFilters(self):
        self._mFilTable = [True for x in range(len(self._mTable.index))]
        return

    # Returns the table with the current mask _mFilTable applied to it.
    # The fuzzy parameter can be used to replaces any entries in a column with there associated entry.
    def getTable(self, columns, **options):
        fuzzy = options.get("fuzzy")
        if not fuzzy:
            return self._mTable.loc[self._mFilTable, columns]
        table = self._mTable.loc[self._mFilTable, columns]
        for column in fuzzy:
            for school in fuzzy[column]:
                table = table.replace({column: fuzzy[column][school]}, school)
        return table

    # Rename the columns to follow camelCase for consistency.
    def _renameColumns(self):
        self._mTable.rename(columns={'job_number': 'jobNumber', 'clone_from': 'cloneFrom', 'man_hours': 'manHours',
                                    'completed_time': 'completedTime', 'created_at': 'createdAt',
                                    'updated_at': 'updatedAt', 'deleted_at': 'deletedAt',
                                    'number_items': 'numberItems'},
                           inplace=True)
        self._mTable.index.rename('jobId', inplace=True)
        return

    # Stored variables
    _mTable = None
    _mFilTable = None
    _mRepo = None


