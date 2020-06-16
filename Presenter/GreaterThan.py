class GreaterThan:
    def __init__(self, parameterPack):
        self.mKey = parameterPack[0]
        self.mValue = parameterPack[1]
        return
    def filter(self, table):
        return table[self.mKey] > self.mValue

    mKey = None
    mValue = None