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
# 99 = halt

_pat_sym='[a-z_][a-z_0-9]*'
_pat_section='(?:\\.'+_pat_sym+')+'

_re_section = re.compile('^' + _pat_section + '$')

_re_line_comment = re.compile('^;.*$')
_re_line_meta = re.compile('^@([a-z]+)[\\s]+([^\\s].*)$')
_re_line_symbol = re.compile('^('+_pat_sym+'):$')
_re_line_instruction = re.compile('^([a-z]+)(?:[\\s]+([^\\s].*)|)$')

_re_arg_imm = re.compile('^((?:[-+]|)[0-9]+)$')
_re_arg_mem = re.compile('^\\[([0-9]+)\\]$')
_re_arg_sym_imm = re.compile('^('+_pat_sym+'|%[a-z]+|\\.)(|[-+]?[0-9]+)$')
_re_arg_sym_mem = re.compile('^\\[('+_pat_sym+'|%[a-z]+|\\.)(|[+-][0-9]+)\\]$')

_instructions = {
    'add': (1, 3),
    'mul': (2, 3),
    'in': (3, 1),
    'out': (4, 1),
    'jt': (5, 2),
    'jf': (6, 2),
    'lt': (7, 3),
    'eq': (8, 3),
    'addsp': (9, 1),
    'halt': (99, 0)
}

_arg_mode_mem = 0
_arg_mode_immediate = 1
_arg_mode_sp_rel = 2

class IntAsmError(Exception):
    pass

def _str_to_int(in_str):
    """
    Convert an integer in string format, or empty string, to an integer.

    Simple helper for int(v, 10), which handles empty strings
    """
    if in_str == '':
        return 0
    return int(in_str, 10)

def _parse_line(line, cur_pc):
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
                    ref, value = match.groups()
                    value = _str_to_int(value)
                    if ref == '%pc':
                        args.append((_arg_mode_immediate, ('.', value + cur_pc)))
                    else:
                        args.append((_arg_mode_immediate, (ref, value)))
                    continue
                match = _re_arg_sym_mem.match(argstr)
                if match:
                    ref, value = match.groups()
                    value = _str_to_int(value)
                    if ref == '%sp':
                        args.append((_arg_mode_sp_rel, (None, value)))
                    elif ref == '%pc':
                        args.append((_arg_mode_mem, ('.', value + cur_pc)))
                    else:
                        args.append((_arg_mode_mem, (ref, value)))
                    continue
                raise IntAsmError("Unknown argument")
        return ('instruction', (mnemonic, args))
    raise IntAsmError("Unknown line")

def _instruction_to_ints(mnemonic, args):
    (opcode, arg_count) = _instructions.get(mnemonic, (None, 0))
    if opcode is None:
        raise IntAsmError("Invalid instruction")
    if len(args) != arg_count:
        raise IntAsmError("Invalid argument count")
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
        cur_pc = None
        if section is not None:
            cur_pc = len(section.data)
        linetype, args = _parse_line(line, cur_pc)
        if linetype is None:
            pass
        elif linetype == 'meta':
            tag, value = args
            if tag == 'section':
                if not _re_section.match(value):
                    raise IntAsmError("Invalid section \"" + value + "\"")
                if elf.sections.get(value):
                    raise IntAsmError("Duplicate section \"" + value + "\"")
                section = IntElfSection()
                elf.sections[value] = section
            elif tag == 'origin':
                if section is None:
                    raise IntAsmError("No section specified")
                if section.origin is not None:
                    raise IntAsmError("Duplicate origin for section")
                if section.data != [] or section.symbols != {}:
                    raise IntAsmError("origin can only be specified before code")
                section.origin = _str_to_int(value)
            else:
                raise IntAsmError("Unknown meta-line: "+line)
        elif linetype == 'symbol':
            name = args
            if section is None:
                raise IntAsmError("No section specified")
            section.symbols[name] = IntElfSymbol(len(section.data))
        elif linetype == 'instruction':
            if section is None:
                raise IntAsmError("No section specified")
            instruction = _instruction_to_ints(*args)
            section.data += instruction
        else:
            raise IntAsmError("Invalid line: "+line)

    return elf