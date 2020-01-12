import pytest
from intutils import merge_intelfs, parse_intelf, output_intelf, IntElfError, IntLDError
from io import StringIO
from intutils.intld_merge import _match_symbol_pattern

prefix = 'tests/fixtures/intld_merge/'

programs = [
    (prefix+'application_single', [prefix+'loader.intelf'])
]

error_intld = [
    (prefix + 'err_duplicate_elf_symbol.intld', [
        prefix + 'err_duplicate_elf_symbol_elf_a.intelf',
        prefix + 'err_duplicate_elf_symbol_elf_b.intelf',
    ], IntElfError),
    (prefix + 'err_duplicate_explicit_symbol.intld', [], IntLDError),
    (prefix + 'err_duplicate_origin.intld', [], IntLDError),
]


@pytest.mark.parametrize("testcase_prefix,extra_elfs", programs)
def test_merge_intelfs(testcase_prefix, extra_elfs):
    elfs = []
    for fname in extra_elfs:
        with open(fname, 'r') as f:
            elfs.append(parse_intelf(f))

    with open(testcase_prefix + '.intelf', 'r') as f:
        elfs.append(parse_intelf(f))

    with open(testcase_prefix + '_dest.intelf', 'r') as f:
        expect = f.read()

    outp = StringIO()
    with open(testcase_prefix + '.intld', 'r') as f_ld:
        out_elf = merge_intelfs(f_ld, elfs)
        output_intelf(out_elf, file=outp)

    assert outp.getvalue().rstrip() == expect.rstrip()


@pytest.mark.parametrize("filename,extra_elfs,exception", error_intld)
def test_merge_intelfs(filename, extra_elfs, exception):
    elfs = []
    for fname in extra_elfs:
        with open(fname, 'r') as f:
            elfs.append(parse_intelf(f))

    with pytest.raises(exception):
        with open(filename, 'r') as f_ld:
            merge_intelfs(f_ld, elfs)


symbol_matches = [
    ('.text.*', '.text', True),
    ('.text.*', '.text.stuff', True),
    ('.text.*', '.text.a.b', True),
    ('.text.*', '.textstuff', False),
    ('.text.*', '.te', False),
    ('.text', '.text', True),
    ('.text', '.text.stuff', False),
    ('.text', '.text.a.b', False),
    ('.text.*', '.data', False),
    ('.text.*', '.data.text', False),
]


@pytest.mark.parametrize("pattern,section,match", symbol_matches)
def test_intld_symbol_match(pattern, section, match):
    assert _match_symbol_pattern(pattern, section) == match
