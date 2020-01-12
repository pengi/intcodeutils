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
        self.data += [(k,(v+offset) if k=='.' else v) for (k,v) in section.data]

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
            if self.origin is not None and rel_name == '.':
                out_section.data.append((None, value + self.origin))
            else:
                rel_value = symbols.get(rel_name)
                if rel_value is not None:
                    out_section.data.append((None, rel_value + value))
                else:
                    out_section.data.append((rel_name, value))
        return out_section
    
    def export(self):
        for rel, _value in self.data:
            if rel is not None:
                raise IntElfError('exporting with unresolved relocation')
        return [value for k,value in self.data]

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

    def export(self):
        length = 0
        for section in self.sections.values():
            if section.origin is None:
                raise IntElfError('exporting with relocatable sections')
            section_end = section.origin + len(section.data)
            if section_end > length:
                length = section_end

        values = [0] * length
        for section in self.sections.values():
            values[section.origin:section.origin+len(section.data)] = section.export()
        return values