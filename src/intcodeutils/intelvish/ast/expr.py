from .helper import str_format


class IntelvishASTExpr:
    def return_bool(self):
        return False


class IntelvishASTExprVar(IntelvishASTExpr):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str_format('expr_var', self.name)

    def simplify(self):
        return IntelvishASTExprVar(self.name)


class IntelvishASTExprConstant(IntelvishASTExpr):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str_format('expr_const', str(self.value))

    def simplify(self):
        return IntelvishASTExprConstant(self.value)


class IntelvishASTExprAdd(IntelvishASTExpr):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return str_format('expr_add', None, [self.lhs, self.rhs])

    def simplify(self):
        lhs = self.lhs.simplify()
        rhs = self.rhs.simplify()
        if type(lhs) == IntelvishASTExprConstant and type(rhs) == IntelvishASTExprConstant:
            return IntelvishASTExprConstant(lhs.value + rhs.value)
        return IntelvishASTExprAdd(lhs, rhs)


class IntelvishASTExprSub(IntelvishASTExpr):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return str_format('expr_sub', None, [self.lhs, self.rhs])

    def simplify(self):
        lhs = self.lhs.simplify()
        rhs = self.rhs.simplify()
        if type(lhs) == IntelvishASTExprConstant and type(rhs) == IntelvishASTExprConstant:
            return IntelvishASTExprConstant(lhs.value - rhs.value)
        return IntelvishASTExprSub(lhs, rhs)


class IntelvishASTExprMul(IntelvishASTExpr):
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
        if type(lhs) == IntelvishASTExprConstant and type(rhs) == IntelvishASTExprConstant:
            return IntelvishASTExprConstant(lhs.value * rhs.value)
        return IntelvishASTExprMul(lhs, rhs)


class IntelvishASTExprLT(IntelvishASTExpr):
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
        return IntelvishASTExprLT(lhs, rhs)


class IntelvishASTExprEQ(IntelvishASTExpr):
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
        return IntelvishASTExprEQ(lhs, rhs)


class IntelvishASTExprNot(IntelvishASTExpr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return str_format('expr_not', None, self.expr)
    
    def return_bool(self):
        return True

    def simplify(self):
        expr = self.expr.simplify()
        if type(expr) == IntelvishASTExprNot and expr.expr.return_bool():
            return expr.expr
        return IntelvishASTExprNot(expr)


class IntelvishASTExprNeg(IntelvishASTExpr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return str_format('expr_neg', None, self.expr)

    def simplify(self):
        if type(self.expr) == IntelvishASTExprConstant:
            return IntelvishASTExprConstant(-self.expr.value)
        return IntelvishASTExprNeg(self.expr.simplify())


class IntelvishASTExprCall(IntelvishASTExpr):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        return str_format('expr_call', self.name, self.args)

    def simplify(self):
        return IntelvishASTExprCall(self.name, [arg.simplify() for arg in self.args])

class IntelvishASTExprAssign(IntelvishASTExpr):
    def __init__(self, dst, expr):
        self.dst = dst
        self.expr = expr

    def __str__(self):
        return str_format('expr_assign', None, [self.dst, self.expr])

    def simplify(self):
        return IntelvishASTExprAssign(self.dst.simplify(), self.expr.simplify())