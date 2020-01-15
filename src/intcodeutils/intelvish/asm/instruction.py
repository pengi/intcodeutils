from .var import VarConst, VarStackRef

class AsmInstr:
    def __init__(self):
        self.ref = None

    def get_ref(self, scope):
        if self.ref is None:
            self.ref = scope.get_id('label')
        return self.ref

    def _refstr(self):
        if self.ref is None:
            return ''
        else:
            return '{}: '.format(self.ref)


class AsmInstrComment(AsmInstr):
    def __init__(self, comment=''):
        super(AsmInstrComment, self).__init__()
        self.comment = comment

    def __str__(self):
        return self._refstr()+'; {}'.format(self.comment)


class AsmInstrNotImplemented(AsmInstr):
    def __init__(self, descr=''):
        super(AsmInstrNotImplemented, self).__init__()
        self.descr = descr

    def __str__(self):
        return self._refstr()+'Not implemented: {}'.format(self.descr)


class AsmInstrBinary(AsmInstr):
    def __init__(self, lhs, rhs, ret):
        super(AsmInstrBinary, self).__init__()
        self.lhs = lhs
        self.rhs = rhs
        self.ret = ret

    def __str__(self):
        return self._refstr()+'{} {}, {}, {}'.format(self.op, self.lhs, self.rhs, self.ret)


class AsmInstrAdd(AsmInstrBinary):
    op = 'add'


class AsmInstrMul(AsmInstrBinary):
    op = 'mul'


class AsmInstrLt(AsmInstrBinary):
    op = 'lt'


class AsmInstrEq(AsmInstrBinary):
    op = 'eq'


class AsmInstrLoad(AsmInstrAdd):
    def __init__(self, src, dst):
        super(AsmInstrLoad, self).__init__(src, VarConst(0, False), dst)


class AsmInstrJumpIfTrue(AsmInstr):
    def __init__(self, cond_var, dest_var):
        super(AsmInstrJumpIfTrue, self).__init__()
        self.cond_var = cond_var
        self.dest_var = dest_var

    def __str__(self):
        return self._refstr()+'jt {}, {}'.format(self.cond_var, self.dest_var)


class AsmInstrJump(AsmInstrJumpIfTrue):
    def __init__(self, dest_var):
        super(AsmInstrJump, self).__init__(VarConst(1, False), dest_var)


class AsmInstrReturn(AsmInstrLoad):
    def __init__(self, var):
        super(AsmInstrReturn, self).__init__(var, VarStackRef(0))
