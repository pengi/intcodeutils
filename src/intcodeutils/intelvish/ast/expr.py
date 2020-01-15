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

    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_expr_var(self, *args, **kvargs)


class ASTExprMemResolve(ASTExpr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return str_format('expr_mem_resolve', None, self.expr)

    def simplify(self):
        return ASTExprMemResolve(self.expr.simplify())

    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_expr_mem_resolve(self, *args, **kvargs)


class ASTExprConstant(ASTExpr):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str_format('expr_const', str(self.value))

    def simplify(self):
        return ASTExprConstant(self.value)

    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_expr_constant(self, *args, **kvargs)


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

    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_expr_add(self, *args, **kvargs)


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

    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_expr_sub(self, *args, **kvargs)


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

    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_expr_mul(self, *args, **kvargs)


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

    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_expr_lt(self, *args, **kvargs)


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

    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_expr_eq(self, *args, **kvargs)


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

    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_expr_not(self, *args, **kvargs)


class ASTExprNeg(ASTExpr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return str_format('expr_neg', None, self.expr)

    def simplify(self):
        if type(self.expr) == ASTExprConstant:
            return ASTExprConstant(-self.expr.value)
        return ASTExprNeg(self.expr.simplify())

    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_expr_neg(self, *args, **kvargs)


class ASTExprCall(ASTExpr):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        return str_format('expr_call', self.name, self.args)

    def simplify(self):
        return ASTExprCall(self.name, [arg.simplify() for arg in self.args])

    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_expr_call(self, *args, **kvargs)


class ASTExprAssign(ASTExpr):
    def __init__(self, dst, expr):
        self.dst = dst
        self.expr = expr

    def __str__(self):
        return str_format('expr_assign', None, [self.dst, self.expr])

    def simplify(self):
        return ASTExprAssign(self.dst.simplify(), self.expr.simplify())

    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_expr_assign(self, *args, **kvargs)