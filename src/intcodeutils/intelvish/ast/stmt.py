from .helper import str_format

class IntelvishASTStmt:
    pass

class IntelvishASTStmtReturn(IntelvishASTStmt):
    def __init__(self, expr):
        self.expr = expr
    
    def __str__(self):
        return str_format('return', None, self.expr)
    
    def simplify(self):
        return IntelvishASTStmtReturn(self.expr.simplify())


class IntelvishASTStmtExpr(IntelvishASTStmt):
    def __init__(self, expr):
        self.expr = expr
    
    def __str__(self):
        return str_format('expr', None, self.expr)
    
    def simplify(self):
        return IntelvishASTStmtExpr(self.expr.simplify())
