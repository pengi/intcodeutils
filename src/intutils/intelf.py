from .model import IntElfFile, IntElfSection, IntElfSymbol
import re
import sys

_pat_sym='[a-z_][a-z_0-9]*'
_pat_section='(?:\\.'+_pat_sym+')+'

_pat_line_section = re.compile('^('+_pat_section+'):(.*)$')
_pat_line_arg = re.compile('^('+_pat_sym+')\\.('+_pat_sym+'):[\\s]*(.*)$')

_pat_val_rel = re.compile('^('+_pat_sym+')([+-][0-9]+|)$')
_pat_val_abs = re.compile('^([+-]?[0-9]+)$')

class IntElfError(Exception):
    pass

def _parse_section(data):
    section = IntElfSection()
    data = data.strip()
    if data != '':
        args = data.split(",")
        for arg in args:
            found = False

            match = _pat_val_rel.match(arg)
            if match:
                found = True
                rel, value = match.groups()
                if value == '':
                    value = 0
                else:
                    value = int(value, 10)
                
                section.data.append((rel,value))

            match = _pat_val_abs.match(arg)
            if match:
                found = True
                value = int(match.group(1), 10)
                
                section.data.append((None,value))
                
            if not found:
                raise IntElfError("Malformed value: " + arg)
    return section

def parse_intelf(f):
    elf = IntElfFile()
    section = None
    for line in f:
        line = line.strip()

        # Ignore empty lines
        if line == '':
            continue

        match = _pat_line_section.match(line)
        if match:
            name, content = match.groups()
            if elf.sections.get(name):
                raise IntElfError("Duplicate section: " + name)
            section = _parse_section(content)
            elf.sections[name] = section
            continue

        match = _pat_line_arg.match(line)
        if match:
            name, arg, val = match.groups()
            if section is None:
                raise IntElfError("Argument without section")
            if name == '_':
                # Section parameter. Only "origin" is supported, ignore others
                if arg == "origin":
                    if section.origin is not None:
                        raise IntElfError("Duplicate origin")
                    section.origin = int(val, 10)
            else:
                # Currently only "offset" is supported, ignore others
                if arg == "offset":
                    if section.symbols.get(name):
                        raise IntElfError("Duplicate symbol: " + name)
                    section.symbols[name] = IntElfSymbol(int(val, 10))
            continue

        raise IntElfError("Invalid line")

    return elf


def output_intelf(elf, file=sys.stdout):
    for name, section in elf.sections.items():
        format_data = []
        for ref, value in section.data:
            if ref is None:
                format_data.append(str(value))
            elif value == 0:
                format_data.append(ref)
            else:
                format_data.append("%s%+d" % (ref, value))
        print("%s: %s" % (name, ",".join(format_data)), file=file)
        if section.origin is not None:
            print("_.origin: %d" % (section.origin,), file=file)
        for name, symbol in section.symbols.items():
            print("%s.offset: %d" % (name, symbol.offset), file=file)
        print(file=file)