import properties as props
from token_class import TokenClass
from error_handling import *


class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node, context):
        # print(f'Found number node: {node}')
        return RuntimeResult().success(
            Number(node.token.value)
                .set_context(context)
                .set_pos(node.pos_start, node.pos_end)
        )

    def visit_BinOpNode(self, node, context):
        # print(f'Found binary operation node: {node}')
        rt_result = RuntimeResult()
        left = rt_result.register(self.visit(node.left_node, context))
        if rt_result.error: return rt_result

        right = rt_result.register(self.visit(node.right_node, context))
        if rt_result.error: return rt_result

        if node.op_token.type == props.TT_PLUS:
            result, error = left.add(right)
        elif node.op_token.type == props.TT_MINUS:
            result, error = left.subtract(right)
        elif node.op_token.type == props.TT_MUL:
            result, error = left.multiply(right)
        elif node.op_token.type == props.TT_DIV:
            result, error = left.divide(right)
        if error:
            return rt_result.failure(error)
        else:
            return rt_result.success(
                result.set_pos(node.pos_start, node.pos_end)
            )

    def visit_UnaryOpNode(self, node, context):
        # print(f'Found unary operation node: {node}')
        rt_result = RuntimeResult()
        number = rt_result.register(self.visit(node.node), context)
        if rt_result.error: return rt_result

        error = None
        if node.op_token.type == props.TT_MINUS:
            number, error = number.multiply(Number(-1))

        if error:
            return rt_result.failure(error)
        else:
            return rt_result.success(number.set_pos(node.pos_start, node.pos_end))


# Values:
class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def add(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subtract(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multiply(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def divide(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RuntimeError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )
            return Number(self.value / other.value).set_context(self.context), None


class RuntimeResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, result):
        if result.error:
            self.error = result.error
        return result.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self


# To create a stack trace for errors let us create a context
class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
