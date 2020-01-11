class IntElfSymbol:
    def __init__(self, offset):
        self.offset = offset

class IntElfSection:
    def __init__(self):
        self.data = []
        self.symbols = {}
        self.origin = None

class IntElfFile:
    def __init__(self):
        self.sections = {}
