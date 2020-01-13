from sly import Lexer, Parser
from .ast import *


class IntelvishError(Exception):
    pass


class IntelvishLexer(Lexer):
    tokens = {NAME, DEF, RETURN, NUMBER, PLUSPLUS, PLUS, MINUS,
              TIMES, DIVIDE, EQ, ASSIGN, LE, LT, GE, GT, NE}
    ignore = r' \t'
    literals = {'(', ')', '{', '}', ';'}

    ignore_newline = r'\n+'
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')
        return t
    
    ignore_comment = r'//.*'

    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    NUMBER = r'[0-9]+'

    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    NAME['def'] = DEF
    NAME['return'] = RETURN

    # Regular expression rules for tokens
    PLUSPLUS = r'\+\+'
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    EQ = r'=='
    ASSIGN = r'='
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'!='

    def error(self, t):
        raise IntelvishError("Lexing error " + repr(t))


class IntelvishParser(Parser):
    tokens = IntelvishLexer.tokens
    
    @_('')
    def elf(self, p):
        print('elf empty')  
        return IntelvishASTFile()

    @_('elf decl')
    def elf(self, p):
        print("elf decl")
        p.elf.add_decl(p.decl)
        return p.elf

    @_('DEF NAME "(" ")" "{" "}"')
    def decl(self, p):
        print("func")
        return IntelvishASTDeclFunc(p.NAME)