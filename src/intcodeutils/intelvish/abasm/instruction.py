from .var import VarConst, VarStackRef

class AbAsmInstr:
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


class AbAsmInstrComment(AbAsmInstr):
    def __init__(self, comment=''):
        super(AbAsmInstrComment, self).__init__()
        self.comment = comment

    def __str__(self):
        return self._refstr()+'; {}'.format(self.comment)


class AbAsmInstrNotImplemented(AbAsmInstr):
    def __init__(self, descr=''):
        super(AbAsmInstrNotImplemented, self).__init__()
        self.descr = descr

    def __str__(self):
        return self._refstr()+'Not implemented: {}'.format(self.descr)


class AbAsmInstrBinary(AbAsmInstr):
    def __init__(self, lhs, rhs, ret):
        super(AbAsmInstrBinary, self).__init__()
        self.lhs = lhs
        self.rhs = rhs
        self.ret = ret

    def __str__(self):
        return self._refstr()+'{} {}, {}, {}'.format(self.op, self.lhs, self.rhs, self.ret)


class AbAsmInstrAdd(AbAsmInstrBinary):
    op = 'add'


class AbAsmInstrMul(AbAsmInstrBinary):
    op = 'mul'


class AbAsmInstrLt(AbAsmInstrBinary):
    op = 'lt'


class AbAsmInstrEq(AbAsmInstrBinary):
    op = 'eq'


class AbAsmInstrLoad(AbAsmInstrAdd):
    def __init__(self, src, dst):
        super(AbAsmInstrLoad, self).__init__(src, VarConst(0, False), dst)


class AbAsmInstrJumpIfTrue(AbAsmInstr):
    def __init__(self, cond_var, dest_var):
        super(AbAsmInstrJumpIfTrue, self).__init__()
        self.cond_var = cond_var
        self.dest_var = dest_var

    def __str__(self):
        return self._refstr()+'jt {}, {}'.format(self.cond_var, self.dest_var)


class AbAsmInstrJump(AbAsmInstrJumpIfTrue):
    def __init__(self, dest_var):
        super(AbAsmInstrJump, self).__init__(VarConst(1, False), dest_var)


class AbAsmInstrReturn(AbAsmInstrLoad):
    def __init__(self, var):
        super(AbAsmInstrReturn, self).__init__(var, VarStackRef(0))
