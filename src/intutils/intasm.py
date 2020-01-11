from .model import IntElfFile, IntElfSection, IntElfSymbol
import re

# Instructions
# 1 = add
# 2 = mul
# 3 = in
# 4 = out
# 5 = jump if not zero
# 6 = jump if zero
# 7 = compare <
# 8 = compare =
# 9 = update SP
# 99 = exit

_pat_line_comment = re.compile('^--.*$')
_pat_line_meta = re.compile('^@([a-z]+)[\\s]+([^\\s].*)$')
_pat_line_symbol = re.compile('^([^\\s]+):$')
_pat_line_instruction = re.compile('^([a-z]+)(?:[\\s]+([^\\s]*)|)$')

_pat_arg_raw = re.compile('^((?:-|)[0-9]+)$')
_pat_arg_abs = re.compile('^\\[([0-9]+)\\]$')
_pat_arg_rel = re.compile('^\\[%sp([+-][0-9]+)\\]$')

_instructions = {
    'add': (1, 3),
    'mul': (2, 3),
    'in': (3, 1),
    'out': (4, 1),
    'jnz': (5, 2),
    'jz': (6, 2),
    'clt': (7, 3),
    'ceq': (8, 3),
    'sp': (9, 1),
    'exit': (99, 0)
}

def _parse_line(line):
    line = line.strip()
    if line == "":
        return (None, None)
    if _pat_line_comment.match(line):
        return (None, None)

    match = _pat_line_meta.match(line)
    if match:
        return ('meta', match.groups())

    match = _pat_line_symbol.match(line)
    if match:
        return ('symbol', match.group(1))

    match = _pat_line_instruction.match(line)
    if match:
        mnemonic, args_str = match.groups()
        args = []
        if args_str:
            for argstr in args_str.split(","):
                argstr = argstr.strip()
                match = _pat_arg_raw.match(argstr)
                if match:
                    args.append(('imm', int(match.group(1), 10)))
                    continue
                match = _pat_arg_abs.match(argstr)
                if match:
                    args.append(('abs', int(match.group(1), 10)))
                    continue
                match = _pat_arg_rel.match(argstr)
                if match:
                    args.append(('rel', int(match.group(1), 10)))
                    continue
                raise Exception("Unknown argument")
        return ('instruction', (mnemonic, args))
    raise Exception("Unknown line")

def _instruction_to_ints(mnemonic, args):
    (opcode, arg_count) = _instructions[mnemonic]
    if len(args) != arg_count:
        raise Exception("Invalid argument count")
    ints = [None]
    modifier_factor = 100
    for (argtype, value) in args:
        ints.append((None, value))
        if argtype == 'abs':
            opcode += modifier_factor * 0
        if argtype == 'imm':
            opcode += modifier_factor * 1
        if argtype == 'rel':
            opcode += modifier_factor * 2
        modifier_factor *= 10
    ints[0] = (None, opcode)
    return ints

def parse_intasm(file):
    symbols = {}
    sections = {}

    section = None
    elf = IntElfFile()

    for line in file:
        linetype, args = _parse_line(line)
        if linetype is None:
            pass
        elif linetype == 'meta':
            tag, value = args
            if tag == 'section':
                section = IntElfSection()
                elf.sections[value] = section
            else:
                raise Exception("Unknown meta-line: "+line)
        elif linetype == 'symbol':
            name = args
            section.symbols[name] = IntElfSymbol(len(section.data))
        elif linetype == 'instruction':
            section.data += _instruction_to_ints(*args)
        else:
            print(linetype, args)

    return elf