from .helper import str_format

class ASTStmt:
    pass

class ASTStmtReturn(ASTStmt):
    def __init__(self, expr):
        self.expr = expr
    
    def __str__(self):
        return str_format('return', None, self.expr)
    
    def simplify(self):
        return ASTStmtReturn(self.expr.simplify())


class ASTStmtExpr(ASTStmt):
    def __init__(self, expr):
        self.expr = expr
    
    def __str__(self):
        return str_format('stmt_expr', None, self.expr)
    
    def simplify(self):
        return ASTStmtExpr(self.expr.simplify())

class ASTStmtWhile(ASTStmt):
    def __init__(self, expr, stmts):
        self.expr = expr
        self.stmts = stmts
    
    def __str__(self):
        return str_format('while', None, {
            'condition': self.expr,
            'statments': self.stmts,
        })
    
    def simplify(self):
        return ASTStmtWhile(self.expr.simplify(), [stmt.simplify() for stmt in self.stmts])

class ASTStmtIf(ASTStmt):
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
        return ASTStmtIf(expr, if_true, if_false)

class ASTStmtVar(ASTStmt):
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return str_format('stmt_var', self.name)
    
    def simplify(self):
        return ASTStmtVar(self.name)