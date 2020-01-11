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

_pat_sym='[a-z_][a-z_0-9]*'
_pat_section='(?:\\.'+_pat_sym+')+'

_re_section = re.compile('^' + _pat_section + '$')

_re_line_comment = re.compile('^--.*$')
_re_line_meta = re.compile('^@([a-z]+)[\\s]+([^\\s].*)$')
_re_line_symbol = re.compile('^([^\\s]+):$')
_re_line_instruction = re.compile('^('+_pat_sym+')(?:[\\s]+([^\\s]*)|)$')

_re_arg_imm = re.compile('^((?:[-+]|)[0-9]+)$')
_re_arg_mem = re.compile('^\\[([0-9]+)\\]$')
_re_arg_sym_imm = re.compile('^('+_pat_sym+')(|[-+]?[0-9]+)$')
_re_arg_sym_mem = re.compile('^\\[('+_pat_sym+')(|[+-][0-9]+)\\]$')
_re_arg_sp_mem = re.compile('^\\[%sp([+-][0-9]+)\\]$')

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

_arg_mode_mem = 0
_arg_mode_immediate = 1
_arg_mode_sp_rel = 2

def _str_to_int(in_str):
    """
    Convert an integer in string format, or empty string, to an integer.

    Simple helper for int(v, 10), which handles empty strings
    """
    if in_str == '':
        return 0
    return int(in_str, 10)

def _parse_line(line):
    line = line.strip()
    if line == "":
        return (None, None)
    if _re_line_comment.match(line):
        return (None, None)

    match = _re_line_meta.match(line)
    if match:
        return ('meta', match.groups())

    match = _re_line_symbol.match(line)
    if match:
        return ('symbol', match.group(1))

    match = _re_line_instruction.match(line)
    if match:
        mnemonic, args_str = match.groups()
        args = []
        if args_str:
            for argstr in args_str.split(","):
                argstr = argstr.strip()
                match = _re_arg_imm.match(argstr)
                if match:
                    args.append((_arg_mode_immediate, (None, _str_to_int(match.group(1)))))
                    continue
                match = _re_arg_mem.match(argstr)
                if match:
                    args.append((_arg_mode_mem, (None, _str_to_int(match.group(1)))))
                    continue
                match = _re_arg_sym_imm.match(argstr)
                if match:
                    args.append((_arg_mode_immediate, (match.group(1), _str_to_int(match.group(2)))))
                    continue
                match = _re_arg_sym_mem.match(argstr)
                if match:
                    args.append((_arg_mode_mem, (match.group(1), _str_to_int(match.group(2)))))
                    continue
                match = _re_arg_sp_mem.match(argstr)
                if match:
                    args.append((_arg_mode_sp_rel, (None, _str_to_int(match.group(1)))))
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
    for (arg_mode, value) in args:
        ints.append(value)
        opcode += modifier_factor * arg_mode
        modifier_factor *= 10
    ints[0] = (None, opcode)
    return ints

def parse_intasm(file):
    section = None
    elf = IntElfFile()

    for line in file:
        linetype, args = _parse_line(line)
        if linetype is None:
            pass
        elif linetype == 'meta':
            tag, value = args
            if tag == 'section':
                if not _re_section.match(value):
                    raise Exception("Invalid section \"" + value +"\"")
                section = IntElfSection()
                elf.sections[value] = section
            else:
                raise Exception("Unknown meta-line: "+line)
        elif linetype == 'symbol':
            name = args
            section.symbols[name] = IntElfSymbol(len(section.data))
        elif linetype == 'instruction':
            instruction = _instruction_to_ints(*args)
            section.data += instruction
        else:
            raise Exception("Invalid line: "+line)

    return elf