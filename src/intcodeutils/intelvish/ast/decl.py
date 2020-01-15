from .helper import str_format
from .error import ASTError

class ASTDecl:
    def __init__(self, name):
        self.name = name


class ASTDeclFunc(ASTDecl):
    def __init__(self, name, args, stmts):
        super(ASTDeclFunc, self).__init__(name)
        self.args = args
        self.stmts = stmts

    def __str__(self):
        return str_format('func', self.name, {'args': self.args, 'stmts': self.stmts})

    def simplify(self):
        return ASTDeclFunc(self.name, self.args[:], [stmt.simplify() for stmt in self.stmts])

    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_decl_func(self, *args, **kvargs)


class ASTDeclVar(ASTDecl):
    def __init__(self, name):
        super(ASTDeclVar, self).__init__(name)

    def __str__(self):
        return str_format('decl_var', self.name)

    def simplify(self):
        return ASTDeclVar(self.name)

    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_decl_func(self, *args, **kvargs)


class ASTFile:
    def __init__(self):
        self.decls = []

    def add_decl(self, decl):
        self.decls.append(decl)

    def __str__(self):
        return str_format('file', None, self.decls)

    def simplify(self):
        out = ASTFile()
        for decl in self.decls:
            out.decls.append(decl.simplify())
        return out

    def visit(self, visitor, *args, **kvargs):
        return visitor.visit_file(self, *args, **kvargs)