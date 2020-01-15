from sly import Lexer, Parser
from .ast import *


class IlvsError(Exception):
    pass


class IlvsLexer(Lexer):
    tokens = {NAME, DEF, VAR, IF, ELSE, WHILE, RETURN, NUMBER, PLUS, MINUS,
              TIMES, EQ, ASSIGN, LE, LT, GE, GT, NE, NOT}
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
    NAME['var'] = VAR
    NAME['return'] = RETURN
    NAME['if'] = IF
    NAME['else'] = ELSE
    NAME['while'] = WHILE
    

    # Regular expression rules for tokens
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    EQ = r'=='
    ASSIGN = r'='
    NOT = r'!'
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    NE = r'!='

    def error(self, t):
        raise IlvsError("Lexing error " + repr(t))


class IlvsParser(Parser):
    tokens = IlvsLexer.tokens
    start = 'top'
    
    precedence = (
          ('right', ASSIGN),
          ('left', LE, LT, GE, GT, NE, EQ),
          ('left', PLUS, MINUS),
          ('left', TIMES),
          ('right', UMINUS, NOT, MEMRESOLVE),
     )

    
    # Top level
    
    @_('')
    def top(self, p):
        return ASTFile()

    @_('top decl')
    def top(self, p):
        p.top.add_decl(p.decl)
        return p.top
    
    
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


    # Declarations

    @_('DEF NAME "(" args ")" "{" stmts "}"')
    def decl(self, p):
        return ASTDeclFunc(p.NAME, p.args, p.stmts)

    @_('VAR NAME ";"')
    def decl(self, p):
        return ASTDeclVar(p.NAME)
        
        
    # Statements

    @_('')
    def stmts(eslf, p):
        return []
        
    @_('stmts stmt')
    def stmts(self, p):
        return p.stmts + [p.stmt]
        
    @_('RETURN expr ";"')
    def stmt(self, p):
        return ASTStmtReturn(p.expr)

    @_('expr ";"')
    def stmt(self, p):
        return ASTStmtExpr(p.expr)
    
    @_('WHILE "(" expr ")" "{" stmts "}"')
    def stmt(self, p):
        return ASTStmtWhile(p.expr, p.stmts)
    
    @_('IF "(" expr ")" "{" stmts "}"')
    def stmt(self, p):
        return ASTStmtIf(p.expr, p.stmts)
    
    @_('IF "(" expr ")" "{" stmts "}" ELSE "{" stmts "}"')
    def stmt(self, p):
        return ASTStmtIf(p.expr, p.stmts0, p.stmts1)

    @_('VAR NAME ";"')
    def stmt(self, p):
        return ASTStmtVar(p.NAME)
    
    # Variables

    @_('NAME')
    def var(self, p):
        return ASTExprVar(p.NAME)

    @_('TIMES NAME')
    def var(self, p):
        return ASTExprMemResolve(ASTExprVar(p.NAME))

    # Hardcode memresolve to require (), to resolve shift/reduce error
    @_('TIMES "(" expr ")" %prec MEMRESOLVE')
    def var(self, p):
        return ASTExprMemResolve(p.expr)
    
    # Expression

    @_('var ASSIGN expr')
    def expr(self, p):
        return ASTExprAssign(p.var, p.expr)
    
    @_('var')
    def expr(self, p):
        return p.var
        
    @_('NUMBER')
    def expr(self, p):
        return ASTExprConstant(p.NUMBER)
        
    @_('expr PLUS expr')
    def expr(self, p):
        return ASTExprAdd(p.expr0, p.expr1)
        
    @_('expr MINUS expr')
    def expr(self, p):
        return ASTExprSub(p.expr0, p.expr1)
        
    @_('expr TIMES expr')
    def expr(self, p):
        return ASTExprMul(p.expr0, p.expr1)
        
    @_('expr LT expr')
    def expr(self, p):
        return ASTExprLT(p.expr0, p.expr1)
        
    @_('expr GT expr')
    def expr(self, p):
        return ASTExprLT(p.expr1, p.expr0)
        
    @_('expr LE expr')
    def expr(self, p):
        return ASTExprNot(ASTExprLT(p.expr1, p.expr0))
        
    @_('expr GE expr')
    def expr(self, p):
        return ASTExprNot(ASTExprLT(p.expr0, p.expr1))
        
    @_('expr EQ expr')
    def expr(self, p):
        return ASTExprEQ(p.expr0, p.expr1)
        
    @_('expr NE expr')
    def expr(self, p):
        return ASTExprNot(ASTExprEQ(p.expr0, p.expr1))
    
    @_('NOT expr')
    def expr(self, p):
        return ASTExprNot(p.expr)
        
    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr
    
    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return ASTExprNeg(p.expr)
        
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
        return ASTExprCall(p.NAME, p.exprs)