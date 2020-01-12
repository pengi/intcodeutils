import pytest
from intcodeutils import parse_intelf, output_intelf
from io import StringIO

prefix = 'tests/fixtures/intcode/'

success_generation_files = [
    prefix + 'single_section',
    prefix + 'single_section_offset',
    prefix + 'multi_section',
]

@pytest.mark.parametrize("testcase", success_generation_files)
def test_intcode_generation_success(testcase):
    with open(testcase + '.intelf', 'r') as f:
        in_elf = parse_intelf(f)

    with open(testcase + '.intcode', 'r') as f:
        expect = f.read()
    
    actual_ints = in_elf.export()
    actual = ",".join([str(value) for value in actual_ints])

    assert actual.rstrip() == expect.rstrip()