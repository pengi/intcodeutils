from .helper import str_format

class IntelvishASTExpr:
    pass

class IntelvishASTExprVar(IntelvishASTExpr):
    def __init__(self, name):
        self.name = name
    
    def __str__(self):
        return str_format('expr_var', self.name);

class IntelvishASTExprConstant(IntelvishASTExpr):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str_format('expr_const', str(self.value));

class IntelvishASTExprAdd(IntelvishASTExpr):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    
    def __str__(self):
        return str_format('expr_add', None, [self.lhs, self.rhs]);

class IntelvishASTExprSub(IntelvishASTExpr):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    
    def __str__(self):
        return str_format('expr_sub', None, [self.lhs, self.rhs]);

class IntelvishASTExprMul(IntelvishASTExpr):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    
    def __str__(self):
        return str_format('expr_mul', None, [self.lhs, self.rhs]);

class IntelvishASTExprNeg(IntelvishASTExpr):
    def __init__(self, expr):
        self.expr = expr
    
    def __str__(self):
        return str_format('expr_neg', None, [self.expr]);

class IntelvishASTExprCall(IntelvishASTExpr):
    def __init__(self, name, args):
        self.name = name
        self.args = args
    
    def __str__(self):
        return str_format('expr_call', self.name, self.args);