from sly import Lexer, Parser
from .ast import *


class IntelvishError(Exception):
    pass


class IntelvishLexer(Lexer):
    tokens = {NAME, DEF, RETURN, NUMBER, PLUSPLUS, PLUS, MINUS,
              TIMES, DIVIDE, EQ, ASSIGN, LE, LT, GE, GT, NE}
    ignore = r' \t'
    literals = {'(', ')', '{', '}', ';', ','}

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
    start = 'elf'
    
    precedence = (
          ('nonassoc', LE, LT, GE, GT, NE, EQ),
          ('left', PLUS, MINUS),
          ('left', TIMES, DIVIDE),
          ('right', UMINUS),
     )

    
    # Top level
    
    @_('')
    def elf(self, p):
        return IntelvishASTFile()

    @_('elf decl')
    def elf(self, p):
        p.elf.add_decl(p.decl)
        return p.elf
    
    
    # Function
    
    @_('NAME')
    def arg(self, p):
        return p.NAME
    
    @_('')
    def args(self, p):
        return []
    
    @_('arg')
    def args(self, p):
        return [p.arg]
        
    @_('args "," arg')
    def args(self, p):
        return p.args + [p.arg]
    
    @_('NAME')
    def stmt(self, p):
        return None

    @_('DEF NAME "(" args ")" "{" stmts "}"')
    def decl(self, p):
        return IntelvishASTDeclFunc(p.NAME, p.args, p.stmts)
        
        
    # Statements

    @_('')
    def stmts(eslf, p):
        return []
        
    @_('stmts stmt')
    def stmts(self, p):
        return p.stmts + [p.stmt]
        
    @_('RETURN expr ";"')
    def stmt(self, p):
        return IntelvishASTStmtReturn(p.expr)
        
    
    # Expression
    
    @_('NAME')
    def expr(self, p):
        return IntelvishASTExprVar(p.NAME)
        
    @_('NUMBER')
    def expr(self, p):
        return IntelvishASTExprConstant(p.NUMBER)
        
    @_('expr PLUS expr')
    def expr(self, p):
        return IntelvishASTExprAdd(p.expr0, p.expr1)
        
    @_('expr MINUS expr')
    def expr(self, p):
        return IntelvishASTExprSub(p.expr0, p.expr1)
        
    @_('expr TIMES expr')
    def expr(self, p):
        return IntelvishASTExprMul(p.expr0, p.expr1)
        
    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr
    
    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return IntelvishASTExprNeg(p.expr)
        
    @_('')
    def exprs(self, p):
        return []
    
    @_('expr')
    def exprs(self, p):
        return [p.expr]
    
    @_('exprs "," expr')
    def exprs(self, p):
        return p.exprs + [p.expr]
        
    @_('NAME "(" exprs ")"')
    def expr(self, p):
        return IntelvishASTExprCall(p.NAME, p.exprs)