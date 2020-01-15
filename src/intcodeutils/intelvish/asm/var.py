class Var:
    rel = None

    def __init__(self, value, deref=True):
        self.value = value
        self.deref = deref

    def __str__(self):
        if self.rel:
            res = "{}+{}".format(self.rel, self.value)
        else:
            res = "{}".format(self.value)
        if self.deref:
            res = "[{}]".format(res)
        return res


class VarStackRef(Var):
    rel = '%callsp'


class VarNextStackRef(Var):
    rel = '%sp'


class VarPcRef(Var):
    rel = '%pc'

class VarInstrRef(Var):
    def __init__(self, ref, offset):
        self.ref = ref
        self.offset = offset
    
    def __str__(self):
        return "{}+{}".format(self.ref, self.offset)

class VarConst(Var):
    rel = None


class VarSym(Var):
    rel = None


class VarMap:
    def __init__(self):
        self.vars = {}
        self.seqno = 0

    def new_anonymous(self):
        self.seqno += 1
        return VarStackRef(self.seqno)

    def new_named(self, name):
        var = self.vars.get(name, None)
        if var is None:
            self.vars[name] = self.new_anonymous()
        return self.vars[name]

    def get_named(self, name):
        return self.vars.get(name, VarSym(name))

    def get_size(self):
        return self.seqno

class Scope:
    def __init__(self):
        self.varmap = VarMap()
        self.counters = {}
    
    def get_id(self, name):
        value = self.counters.get(name, 0)
        self.counters[name] = value+1
        return '{}_{}'.format(name, value)