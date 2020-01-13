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