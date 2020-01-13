from .helper import str_format


class IntelvishASTDecl:
    def __init__(self, name):
        self.name = name


class IntelvishASTDeclFunc(IntelvishASTDecl):
    def __init__(self, name, args, stmts):
        super(IntelvishASTDeclFunc, self).__init__(name)
        self.args = args
        self.stmts = stmts

    def __str__(self):
        return str_format('func', self.name, {'args': self.args, 'stmts': self.stmts})

    def simplify(self):
        return IntelvishASTDeclFunc(self.name, self.args[:], [stmt.simplify() for stmt in self.stmts])

class IntelvishASTDeclVar(IntelvishASTDecl):
    def __init__(self, name):
        super(IntelvishASTDeclVar, self).__init__(name)
    
    def __str__(self):
        return str_format('decl_var', self.name)
    
    def simplify(self):
        return IntelvishASTDeclVar(self.name)


class IntelvishASTFile:
    def __init__(self):
        self.decls = []

    def add_decl(self, decl):
        self.decls.append(decl)

    def __str__(self):
        return str_format('file', None, self.decls)

    def simplify(self):
        out = IntelvishASTFile()
        for decl in self.decls:
            out.decls.append(decl.simplify())
        return out