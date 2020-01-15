class AsmFile:
    def __init__(self):
        self.vars = {}
        self.funcs = {}

    def add_var(self, var):
        print("Add var: " + var)

    def add_func(self, func):
        print("Add func: {}".format(func.name))
        for stmt in func.instrs:
            print(" - {}".format(stmt))
