def _tostrhelper(nodetype, name, children):
    outp = nodetype;
    if name is not None:
        outp += ' ' + name
    if type(children) == dict:
        outp += ' {\n'
        for name, items in children.items():
            outp += '  ' + name + ':\n'
            for item in items:
                outp += '    ' + str(item).replace('\n', '\n    ') + '\n'
        outp += '}'
    elif type(children) == list:
        outp += ' [\n'
        for item in children:
            outp += '  ' + str(item).replace('\n', '\n  ') + '\n'
        outp += ']'
    return outp

class IntelvishASTDecl:
    def __init__(self, name):
        self.name = name

class IntelvishASTDeclFunc(IntelvishASTDecl):
    def __init__(self, name, args, stmts):
        super(IntelvishASTDeclFunc, self).__init__(name)
        self.args = args
        self.stmts = stmts

    def __str__(self):
        return _tostrhelper('func', self.name, {'args': self.args, 'stmts': self.stmts})

class IntelvishASTExpr:
    def __init__(self, parts):
        self.parts = parts
    
    def __str__(self):
        return _tostrhelper('expr', None, self.parts)

class IntelvishASTStmt:
    def __init__(self, parts):
        self.parts = parts
    
    def __str__(self):
        return _tostrhelper('stmt', None, self.parts)

class IntelvishASTFile:
    def __init__(self):
        self.decls = []
    
    def add_decl(self, decl):
        self.decls.append(decl)
    
    def __str__(self):
        return _tostrhelper('file', None, self.decls)