def _tostrhelper(type, name, children):
    outp = type;
    if name is not None:
        outp += ' ' + name
    outp += ' {\n'
    for name, items in children.items():
        outp += '  ' + name + ':\n'
        for item in items:
            outp += '  - ' + str(item).replace('\n', '\n    ') + '\n'
    outp += '}'
    return outp

class IntelvishASTDecl:
    def __init__(self, name):
        self.name = name

class IntelvishASTDeclFunc(IntelvishASTDecl):
    def __str__(self):
        return _tostrhelper('func', self.name, {})

class IntelvishASTFile:
    def __init__(self):
        self.decls = []
    
    def add_decl(self, decl):
        self.decls.append(decl)
    
    def __str__(self):
        return _tostrhelper('file', None, {'decls': self.decls})