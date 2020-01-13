import pytest
from intcodeutils.intelvish import IntelvishParser, IntelvishLexer, IntelvishError

prefix = 'tests/intelvish/fixtures/'

success_files = [
    prefix + 'single_func',
]

def test_lexing():
    input = """
    def func() {
        i++;
        stuff = kalle - pelle; // Comment
        return 12;
    }
    """
    expect = [
        'DEF', 'NAME', '(', ')', '{', 'NAME', 'PLUSPLUS', ';', 'NAME',
        'ASSIGN', 'NAME', 'MINUS', 'NAME', ';', 'RETURN', 'NUMBER', ';', '}'
    ]

    lexer = IntelvishLexer()
    count = 0
    for lex_tok, exp_tok in zip(lexer.tokenize(input), expect):
        assert lex_tok.type == exp_tok
        count += 1
    assert count == len(expect)


@pytest.mark.parametrize("testcase", success_files)
def test_parsing(testcase):
    lexer = IntelvishLexer()
    parser = IntelvishParser()
    with open(testcase+'.intelvish', 'r') as f:
        elf = parser.parse(lexer.tokenize(f.read()))
    
    with open(testcase+'.ast', 'r') as f:
        expect_ast = f.read()
    assert expect_ast == str(elf)