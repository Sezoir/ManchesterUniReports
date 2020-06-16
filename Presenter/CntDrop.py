# Filter: Drop all jobs with relation to a categorical data, where the categorical data has in total less than parameter given.
class CntDrop:
    def __init__(self, parameterPack):
        self.mKey = parameterPack[0]
        self.mValue = parameterPack[1]
        return
    def filter(self, table):
        # Get all unique keys
        uniqueKeys = table[self.mKey].unique()
        cnt = table[self.mKey].value_counts(dropna=False).to_dict()
        # Get array for true values
        mask = [True for x in table.index]
        print(cnt)
        # Drop all keys with less than minimum count
        for key in uniqueKeys:
            if cnt[key] < self.mValue:
                mask = mask & (table[self.mKey] != key)
        return mask

    mKey = None
    mValue = None