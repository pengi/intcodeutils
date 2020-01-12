class IntElfError(Exception):
    pass

class IntElfSymbol:
    def __init__(self, offset):
        self.offset = offset
    
    def clone(self, offset=0):
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
            self.symbols[name] = symbol.clone(offset)

    def clone_resolve_symbols(self, symbols):
        out_section = IntElfSection()
        for name, sym in self.symbols.items():
            out_section.symbols[name] = sym.clone()
        out_section.origin = self.origin
        for rel_name, value in self.data:
            rel_value = symbols.get(rel_name)
            if rel_value is not None:
                out_section.data.append((None, rel_value + value))
            else:
                out_section.data.append((rel_name, value))
        return out_section

class IntElfFile:
    def __init__(self):
        self.sections = {}
    
    def clone_resolve_symbols(self):
        absolute_symbols = {}

        for section in self.sections.values():
            # If section is relocatable, the symbols cant be resolved
            if section.origin is None:
                continue

            for symbol_name, symbol in section.symbols.items():
                absolute_symbols[symbol_name] = symbol.offset + section.origin
        
        out_elf = IntElfFile()
        for section_name, section in self.sections.items():
            out_elf.sections[section_name] = section.clone_resolve_symbols(absolute_symbols)
        
        return out_elf
