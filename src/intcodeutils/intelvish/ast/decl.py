from .helper import str_format


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

class ASTDeclVar(ASTDecl):
    def __init__(self, name):
        super(ASTDeclVar, self).__init__(name)
    
    def __str__(self):
        return str_format('decl_var', self.name)
    
    def simplify(self):
        return ASTDeclVar(self.name)


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