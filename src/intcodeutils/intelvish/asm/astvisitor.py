from .file import AsmFile
from .block import AsmFunc
from .instruction import AsmInstrComment, AsmInstrNotImplemented, AsmInstrAdd, AsmInstrMul, AsmInstrLt, AsmInstrEq, AsmInstrLoad, AsmInstrJumpIfTrue, AsmInstrReturn

from .var import Scope, VarConst, VarInstrRef

from ..ast import ASTDeclVar, ASTDeclFunc

class AsmASTVisitor:
    def __init__(self):
        pass

    def visit_file(self, node):
        abasm = AsmFile()
        for decl in node.decls:
            if type(decl) is ASTDeclVar:
                abasm.add_var(decl.visit(self, ))
            elif type(decl) is ASTDeclFunc:
                abasm.add_func(decl.visit(self, ))
            else:
                raise ASTError('Unknown declaration')
        return abasm

    def visit_decl_func(self, node):
        scope = Scope()
        lin_args = [scope.varmap.new_named(arg) for arg in node.args]

        lin_stmts = []
        for stmt in node.stmts:
            lin_stmts += stmt.visit(self, scope)

        return AsmFunc(node.name, lin_args, lin_stmts)

    def visit_decl_var(self, node):
        return node.name

    def visit_expr_var(self, node, scope):
        return scope.varmap.get_named(node.name), []

    def visit_expr_mem_resolve(self, node, scope):
        expr_ret, expr_stmts = node.expr.visit(self, scope)
        ret_var = scope.varmap.new_anonymous()

        read_instr = AsmInstrLoad(VarConst(0), ret_var)
        return ret_var, expr_stmts + [
            AsmInstrLoad(expr_ret, VarInstrRef(
                read_instr.get_ref(scope), 1)),
            read_instr,
        ]

    def visit_expr_constant(self, node, scope):
        return VarConst(node.value, False), []

    def visit_expr_add(self, node, scope):
        lhs_ret, lhs_stmts = node.lhs.visit(self, scope)
        rhs_ret, rhs_stmts = node.rhs.visit(self, scope)
        ret_var = scope.varmap.new_anonymous()
        return ret_var, lhs_stmts + rhs_stmts + [AsmInstrAdd(lhs_ret, rhs_ret, ret_var)]

    def visit_expr_sub(self, node, scope):
        lhs_ret, lhs_stmts = node.lhs.visit(self, scope)
        rhs_ret, rhs_stmts = node.rhs.visit(self, scope)
        ret_var = scope.varmap.new_anonymous()
        return ret_var, lhs_stmts + rhs_stmts + [
            AsmInstrMul(VarConst(-1), rhs_ret, rhs_ret),
            AsmInstrAdd(lhs_ret, rhs_ret, ret_var)
        ]

    def visit_expr_mul(self, node, scope):
        lhs_ret, lhs_stmts = node.lhs.visit(self, scope)
        rhs_ret, rhs_stmts = node.rhs.visit(self, scope)
        ret_var = scope.varmap.new_anonymous()
        return ret_var, lhs_stmts + rhs_stmts + [
            AsmInstrMul(lhs_ret, rhs_ret, ret_var)
        ]

    def visit_expr_lt(self, node, scope):
        lhs_ret, lhs_stmts = node.lhs.visit(self, scope)
        rhs_ret, rhs_stmts = node.rhs.visit(self, scope)
        ret_var = scope.varmap.new_anonymous()
        return ret_var, lhs_stmts + rhs_stmts + [
            AsmInstrLt(lhs_ret, rhs_ret, ret_var)
        ]

    def visit_expr_eq(self, node, scope):
        lhs_ret, lhs_stmts = node.lhs.visit(self, scope)
        rhs_ret, rhs_stmts = node.rhs.visit(self, scope)
        ret_var = scope.varmap.new_anonymous()
        return ret_var, lhs_stmts + rhs_stmts + [
            AsmInstrEq(lhs_ret, rhs_ret, ret_var)
        ]

    def visit_expr_not(self, node, scope):
        expr_ret, expr_stmts = node.expr.visit(self, scope)
        ret_var = scope.varmap.new_anonymous()
        return ret_var, expr_stmts + [
            AsmInstrEq(VarConst(0), expr_ret, ret_var)
        ]

    def visit_expr_neg(self, node, scope):
        expr_ret, expr_stmts = node.expr.visit(self, scope)
        ret_var = scope.varmap.new_anonymous()
        return ret_var, expr_stmts + [
            AsmInstrMul(VarConst(-1), expr_ret, ret_var)
        ]

    def visit_expr_call(self, node, scope):
        stmts = []
        arg_load_stmts = []

        for i, arg in enumerate(node.args):
            arg_var, arg_stmts = arg.visit(self, scope)
            stmts += arg_stmts
            arg_load_stmts.append(AsmInstrLoad(
                arg_var, VarNextStackRef(i+1)))

        ret_var = scope.varmap.new_anonymous()

        load_instr = AsmInstrLoad(VarNextStackRef(0), ret_var)

        return ret_var, stmts + arg_load_stmts + [
            AsmInstrLoad(VarInstrRef(
                load_instr.get_ref(scope), 0), VarNextStackRef(0)),
            AsmInstrJump(VarSym(node.name, False)),
            load_instr
        ]

    def visit_expr_assign(self, node, scope):
        expr_ret, expr_stmts = node.expr.visit(self, scope)
        dst_ret, dst_stmts = node.dst.visit(self, scope)
        return node.dst, expr_stmts + dst_stmts + [
            AsmInstrLoad(expr_ret, dst_ret)
        ]

    def visit_stmt_return(self, node, scope):
        ret_var, stmts = node.expr.visit(self, scope)
        return stmts + [AsmInstrReturn(ret_var)]

    def visit_stmt_expr(self, node, scope):
        # Don't care about result
        _, stmts = node.expr.visit(self, scope)
        return stmts

    def visit_stmt_while(self, node, scope):
        # TODO: Implement
        return []

    def visit_stmt_if(self, node, scope):
        # TODO: Implement
        return []

    def visit_stmt_var(self, node, scope):
        scope.varmap.new_named(node.name)
        return []


def compile_ast(ast):
    return ast.visit(AsmASTVisitor())
