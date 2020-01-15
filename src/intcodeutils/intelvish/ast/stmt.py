from .helper import str_format

class ASTStmt:
    def linearize(self, varmap):
        return []

class ASTStmtReturn(ASTStmt):
    def __init__(self, expr):
        self.expr = expr
    
    def __str__(self):
        return str_format('return', None, self.expr)
    
    def simplify(self):
        return ASTStmtReturn(self.expr.simplify())
        
    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_stmt_return(self, *args, **kvargs)


class ASTStmtExpr(ASTStmt):
    def __init__(self, expr):
        self.expr = expr
    
    def __str__(self):
        return str_format('stmt_expr', None, self.expr)
    
    def simplify(self):
        return ASTStmtExpr(self.expr.simplify())
        
    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_stmt_expr(self, *args, **kvargs)

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
    
    def linearize(self, scope):
        # TODO: Implement
        return []
        
    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_stmt_while(self, *args, **kvargs)

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
        
    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_stmt_if(self, *args, **kvargs)

class ASTStmtVar(ASTStmt):
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return str_format('stmt_var', self.name)
    
    def simplify(self):
        return ASTStmtVar(self.name)
        
    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_stmt_var(self, *args, **kvargs)