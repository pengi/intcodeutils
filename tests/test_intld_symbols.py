import pytest
from intcodeutils import parse_intelf, output_intelf
from io import StringIO

prefix = 'tests/fixtures/intld_symbols/'

success_files = [
    prefix + 'single_section',
    prefix + 'multi_section',
    prefix + 'partial_relocatable',
    prefix + 'section_relative',
]

@pytest.mark.parametrize("testcase", success_files)
def test_intld_symbols_success(testcase):
    with open(testcase + '_in.intelf', 'r') as f:
        in_elf = parse_intelf(f)

    with open(testcase + '_out.intelf', 'r') as f:
        expect = f.read()
    
    actual_elf = in_elf.clone_resolve_symbols()

    outp = StringIO()
    output_intelf(actual_elf, file=outp)

    assert outp.getvalue().rstrip() == expect.rstrip()