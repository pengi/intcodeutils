from .helper import str_format


class ASTExpr:
    def return_bool(self):
        return False


class ASTExprVar(ASTExpr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str_format('expr_var', self.name)

    def simplify(self):
        return ASTExprVar(self.name)


class ASTExprMemResolve(ASTExpr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return str_format('expr_mem_resolve', None, self.expr)

    def simplify(self):
        return ASTExprMemResolve(self.expr.simplify())


class ASTExprConstant(ASTExpr):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str_format('expr_const', str(self.value))

    def simplify(self):
        return ASTExprConstant(self.value)


class ASTExprAdd(ASTExpr):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return str_format('expr_add', None, [self.lhs, self.rhs])

    def simplify(self):
        lhs = self.lhs.simplify()
        rhs = self.rhs.simplify()
        if type(lhs) == ASTExprConstant and type(rhs) == ASTExprConstant:
            return ASTExprConstant(lhs.value + rhs.value)
        return ASTExprAdd(lhs, rhs)


class ASTExprSub(ASTExpr):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return str_format('expr_sub', None, [self.lhs, self.rhs])

    def simplify(self):
        lhs = self.lhs.simplify()
        rhs = self.rhs.simplify()
        if type(lhs) == ASTExprConstant and type(rhs) == ASTExprConstant:
            return ASTExprConstant(lhs.value - rhs.value)
        return ASTExprSub(lhs, rhs)


class ASTExprMul(ASTExpr):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return str_format('expr_mul', None, [self.lhs, self.rhs])

    def return_bool(self):
        return self.lhs.return_bool() and self.rhs.return_bool()

    def simplify(self):
        lhs = self.lhs.simplify()
        rhs = self.rhs.simplify()
        if type(lhs) == ASTExprConstant and type(rhs) == ASTExprConstant:
            return ASTExprConstant(lhs.value * rhs.value)
        return ASTExprMul(lhs, rhs)


class ASTExprLT(ASTExpr):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return str_format('expr_lt', None, [self.lhs, self.rhs])
    
    def return_bool(self):
        return True

    def simplify(self):
        lhs = self.lhs.simplify()
        rhs = self.rhs.simplify()
        return ASTExprLT(lhs, rhs)


class ASTExprEQ(ASTExpr):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return str_format('expr_eq', None, [self.lhs, self.rhs])
    
    def return_bool(self):
        return True

    def simplify(self):
        lhs = self.lhs.simplify()
        rhs = self.rhs.simplify()
        return ASTExprEQ(lhs, rhs)


class ASTExprNot(ASTExpr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return str_format('expr_not', None, self.expr)
    
    def return_bool(self):
        return True

    def simplify(self):
        expr = self.expr.simplify()
        if type(expr) == ASTExprNot and expr.expr.return_bool():
            return expr.expr
        return ASTExprNot(expr)


class ASTExprNeg(ASTExpr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return str_format('expr_neg', None, self.expr)

    def simplify(self):
        if type(self.expr) == ASTExprConstant:
            return ASTExprConstant(-self.expr.value)
        return ASTExprNeg(self.expr.simplify())


class ASTExprCall(ASTExpr):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        return str_format('expr_call', self.name, self.args)

    def simplify(self):
        return ASTExprCall(self.name, [arg.simplify() for arg in self.args])

class ASTExprAssign(ASTExpr):
    def __init__(self, dst, expr):
        self.dst = dst
        self.expr = expr

    def __str__(self):
        return str_format('expr_assign', None, [self.dst, self.expr])

    def simplify(self):
        return ASTExprAssign(self.dst.simplify(), self.expr.simplify())