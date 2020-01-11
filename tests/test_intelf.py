import pytest
from intutils import output_intelf, parse_intelf, IntElfError
import sys
from io import StringIO

prefix = 'tests/fixtures/intelf/'

# Elffiles holding the same structure, so content can be asserted upon
simple_elffiles = [
    prefix+'simple_plain.intelf',
    prefix+'simple_unknown_vars.intelf'
]

# Elffiles holding the output format (with exception of possible linebreaks at end)
plain_elffiles = [
    prefix+'simple_plain.intelf',
    prefix+'non_relocatable.intelf',
    prefix+'empty_section.intelf'
]

err_elffiles = [
    (prefix+'err_no_sym_argument.intelf', IntElfError),
    (prefix+'err_invalid_line.intelf', IntElfError),
    (prefix+'err_duplicate_sections.intelf', IntElfError),
    (prefix+'err_duplicate_symbols.intelf', IntElfError),
    (prefix+'err_symbol_without_section.intelf', IntElfError),
    (prefix+'err_malformed_var_plus_plus.intelf', IntElfError),
    (prefix+'err_malformed_empty.intelf', IntElfError),
    (prefix+'err_duplicate_origin.intelf', IntElfError),
]

@pytest.mark.parametrize("filename", simple_elffiles)
def test_parse_intelf(filename):
    with open(filename, 'r') as f:
        elf = parse_intelf(f)
        assert len(elf.sections) == 2
        assert elf.sections.get('.text')
        assert elf.sections.get('.data')
        assert not elf.sections.get('.doesntexist')
        
        assert len(elf.sections['.text'].data) == 7
        assert elf.sections['.text'].data[0] == (None, 1)
        assert elf.sections['.text'].data[1] == (None, 2)
        assert elf.sections['.text'].data[2] == (None, 3)
        assert elf.sections['.text'].data[3] == ('func1', 4)
        assert elf.sections['.text'].data[4] == ('func2', 0)
        assert elf.sections['.text'].data[5] == ('var', 3)
        assert elf.sections['.text'].data[6] == ('var', -3)
        
        assert len(elf.sections['.text'].symbols) == 3
        assert elf.sections['.text'].symbols['main'].offset == 0
        assert elf.sections['.text'].symbols['func1'].offset == 3
        assert elf.sections['.text'].symbols['func2'].offset == -2

@pytest.mark.parametrize("filename", plain_elffiles)
def test_output_intelf(filename):
    with open(filename, 'r') as file:
        expect = file.read()
    with open(filename, 'r') as file:
        elf = parse_intelf(file)
        outp = StringIO()
        output_intelf(elf, file=outp)
        assert outp.getvalue().rstrip() == expect.rstrip()

def test_non_relocatable():
    with open(prefix+'non_relocatable.intelf', 'r') as f:
        elf = parse_intelf(f)
        
        assert elf.sections.get('.text')
        text = elf.sections['.text']
        assert text.origin == 0
        
        assert elf.sections.get('.data')
        text = elf.sections['.data']
        assert text.origin == 1000

@pytest.mark.parametrize("intelf_file,exception", err_elffiles)
def test_error_intasm(intelf_file,exception):
    with pytest.raises(exception):
        with open(intelf_file, 'r') as intelf:
            parse_intelf(intelf)
