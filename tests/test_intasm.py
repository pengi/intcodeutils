import pytest
from intutils import output_intelf
from intutils import parse_intasm, IntAsmError
from io import StringIO


# Elffiles holding the same structure, so content can be asserted upon
matching_intasm = [
    'tests/fixtures/intasm/no_refs.intasm',
    'tests/fixtures/intasm/with_refs.intasm',
    'tests/fixtures/intasm/multi_section.intasm',
    'tests/fixtures/intasm/non_relocatable.intasm',
]

error_intasm = [
    ('tests/fixtures/intasm/err_code_without_section.intasm', IntAsmError),
    ('tests/fixtures/intasm/err_duplicate_origin.intasm', IntAsmError),
    ('tests/fixtures/intasm/err_invalid_arguments.intasm', IntAsmError),
    ('tests/fixtures/intasm/err_invalid_instruction.intasm', IntAsmError),
    ('tests/fixtures/intasm/err_invalid_line.intasm', IntAsmError),
    ('tests/fixtures/intasm/err_invalid_meta.intasm', IntAsmError),
    ('tests/fixtures/intasm/err_invalid_section.intasm', IntAsmError),
    ('tests/fixtures/intasm/err_multi_section.intasm', IntAsmError),
    ('tests/fixtures/intasm/err_origin_after_instructions.intasm', IntAsmError),
    ('tests/fixtures/intasm/err_origin_after_labels.intasm', IntAsmError),
    ('tests/fixtures/intasm/err_symbol_without_section.intasm', IntAsmError),
]

@pytest.mark.parametrize("intasm_file", matching_intasm)
def test_parse_intasm(intasm_file):
    intelf_file = intasm_file[:-7] + ".intelf"
    print("Running test:", intelf_file, intasm_file)
    expect = "invalid expect"
    actual = "invalid actual"

    with open(intelf_file, 'r') as intelf:
        expect = intelf.read().rstrip()

    with open(intasm_file, 'r') as intasm:
        elf = parse_intasm(intasm)
        outp = StringIO()
        output_intelf(elf, file=outp)
        actual = outp.getvalue().rstrip()

    assert actual == expect

@pytest.mark.parametrize("intasm_file,exception", error_intasm)
def test_error_intasm(intasm_file,exception):
    with pytest.raises(exception):
        with open(intasm_file, 'r') as intasm:
            parse_intasm(intasm)
