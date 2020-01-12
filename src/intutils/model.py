class IntElfError(Exception):
    pass

class IntElfSymbol:
    def __init__(self, offset):
        self.offset = offset
    
    def clone_offset(self, offset):
        return IntElfSymbol(self.offset + offset)

class IntElfSection:
    def __init__(self):
        self.data = []
        self.symbols = {}
        self.origin = None

    def append_section(self, section):
        if section.origin is not None:
            raise IntElfError('appending non-relocatable section')

        offset = len(self.data)
        self.data += [(k,v) for (k,v) in section.data]

        for name, symbol in section.symbols.items():
            if self.symbols.get(name):
                raise IntElfError('symbol already defined: ' + name)
            self.symbols[name] = symbol.clone_offset(offset)

class IntElfFile:
    def __init__(self):
        self.sections = {}
