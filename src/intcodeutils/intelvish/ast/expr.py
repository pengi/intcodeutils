from .helper import str_format

class IntelvishASTExpr:
    def __init__(self, parts):
        self.parts = parts
    
    def __str__(self):
        return str_format('expr', None, self.parts)

class IntelvishASTFile:
    def __init__(self):
        self.decls = []
    
    def add_decl(self, decl):
        self.decls.append(decl)
    
    def __str__(self):
        return str_format('file', None, self.decls)