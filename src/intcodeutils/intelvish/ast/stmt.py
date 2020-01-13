from .helper import str_format

class IntelvishASTStmt:
    def __init__(self, parts):
        self.parts = parts
    
    def __str__(self):
        return str_format('stmt', None, self.parts)