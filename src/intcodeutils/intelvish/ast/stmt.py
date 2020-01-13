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
        return str_format('stmt_expr', None, self.expr)
    
    def simplify(self):
        return IntelvishASTStmtExpr(self.expr.simplify())

class IntelvishASTStmtWhile(IntelvishASTStmt):
    def __init__(self, expr, stmts):
        self.expr = expr
        self.stmts = stmts
    
    def __str__(self):
        return str_format('while', None, {
            'condition': self.expr,
            'statments': self.stmts,
        })
    
    def simplify(self):
        return IntelvishASTStmtWhile(self.expr.simplify(), [stmt.simplify() for stmt in self.stmts])

class IntelvishASTStmtIf(IntelvishASTStmt):
    def __init__(self, expr, if_true, if_false = None):
        self.expr = expr
        self.if_true = if_true
        self.if_false = if_false
    
    def __str__(self):
        return str_format('if', None, {
            'condition': self.expr,
            'if_true': self.if_true,
            'if_false': self.if_false,
        })
    
    def simplify(self):
        expr = self.expr.simplify()
        if_true = [stmt.simplify() for stmt in self.if_true]
        if_false = None
        if self.if_false is not None:
            if_false = [stmt.simplify() for stmt in self.if_false]
        return IntelvishASTStmtIf(expr, if_true, if_false)