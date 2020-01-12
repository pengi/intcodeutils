from .model import IntElfFile, IntElfSection, IntElfSymbol
import re

_pat_sym='[a-z_][a-z_0-9]*'
_pat_section='(?:\\.'+_pat_sym+')+'

_re_line_section = re.compile('^('+_pat_section+'):$')
_re_line_operation = re.compile('^([a-z]+)[\\s]+(.*)$')

class IntLDError(Exception):
    pass

def _match_symbol_pattern(pattern, symbol):
    if pattern[-2:] == '.*':
        if symbol == pattern[:-2]:
            return True
        return symbol[:len(pattern)-1] == pattern[:-1]
    return pattern == symbol

def merge_intelfs(ldfile, elfs):
    elf = IntElfFile()
    section = None

    for line in ldfile:
        line = line.strip()

        match = _re_line_section.match(line)
        if match:
            name, = match.groups()
            if elf.sections.get(name):
                raise IntLDError("Duplicate section: " + name)
            section = IntElfSection()
            elf.sections[name] = section
            continue

        match = _re_line_operation.match(line)
        if match:
            op, value = match.groups()

            if op == 'origin':
                if section.origin is not None:
                    raise IntLDError('Duplicate origin specified')
                section.origin = int(value, 10)
            elif op == 'load':
                for srcelf in elfs:
                    for src_name, src_section in srcelf.sections.items():
                        if _match_symbol_pattern(value, src_name):
                            section.append_section(src_section)
            elif op == 'sym':
                if section.symbols.get(value):
                    raise IntLDError('Synmbol already specified: '+value)
                section.symbols[value] = IntElfSymbol(len(section.data))
            else:
                raise IntLDError('Invalid operator: ' + op)
            continue

        print(repr(line.strip()))

    return elf