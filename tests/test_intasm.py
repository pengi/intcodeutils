import pytest
from intutils import output_intelf
from intutils import parse_intasm
import sys
from io import StringIO


# Elffiles holding the same structure, so content can be asserted upon
matching_intelf = [
    'tests/fixtures/intasm/no_refs.intasm',
    'tests/fixtures/intasm/with_refs.intasm',
    'tests/fixtures/intasm/multi_section.intasm',
]

@pytest.mark.parametrize("intasm_file", matching_intelf)
def test_parse_intelf(intasm_file):
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