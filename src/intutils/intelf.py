from .model import IntElfFile, IntElfSection, IntElfSymbol
import re
import sys

_pat_section = re.compile('^[\\s]*(\\.[a-z0-9\\.-_]+):[\\s]*(.*[^\\s])[\\s]*$')
_pat_arg = re.compile('^[\\s]*([a-z0-9]+)\\.([a-z0-9]+):[\\s]*(.*[^\\s])[\\s]*$')

_pat_val_rel = re.compile('^[\\s]*([a-z][a-z0-9]*)[\\s]*([+-][\\s]*[0-9]+|)[\\s]*$')
_pat_val_abs = re.compile('^[\\s]*([+-]?[\\s]*[0-9]+)[\\s]*$')

def _parse_section(data):
    args = data.split(",")
    section = IntElfSection()
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
            # Error
            pass
    return section

def parse_intelf(f):
    elf = IntElfFile()
    section = None
    for line in f:
        match = _pat_section.match(line)
        if match:
            name, content = match.groups()
            section = _parse_section(content)
            elf.sections[name] = section
        match = _pat_arg.match(line)
        if match:
            name, arg, val = match.groups()
            if name == '_':
                # Section parameter, ignore all for now
                pass
            else:
                # Currently only "offset" is supported, ignore others
                if arg == "offset":
                    section.symbols[name] = IntElfSymbol(int(val, 10))
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
        for name, symbol in section.symbols.items():
            print("%s.offset: %d" % (name, symbol.offset), file=file)
        print(file=file)