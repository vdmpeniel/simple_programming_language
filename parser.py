import properties as props
from token import Token
from error_handling import *


# NODES
class NumberNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.token}'


class BinOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.op_token}, {self.right_node})'


class UnaryOpNode:
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

    def __repr__(self):
        return f'({self.op_token}, {self.node})'


# PARSER
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = -1
        self.current_token = tokens[0]
        self.advance()

    def parse(self):
        result = self.expression()
        if not result.error and self.current_token.type != props.TT_EOF:
            return result.failure(InvalidSyntaxError(
                self.current_token.pos_start,
                self.current_token.pos_end,
                "Expected '+', '-', '*', or '/'"
            ))
        return result

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def factor(self):
        result = ParseResult()
        token = self.current_token

        if token.type in (props.TT_PLUS, props.TT_MINUS):
            result.register(self.advance())
            factor = result.register(self.factor())
            if result.error:
                return result
            return result.success(UnaryOpNode(token, factor))

        elif token.type in (props.TT_INT, props.TT_FLOAT):
            result.register(self.advance())
            return result.success(NumberNode(token))

        elif token.type == props.TT_LPAREN:
            result.register(self.advance())
            expression = result.register(self.expression())
            if result.error:
                return result
            if self.current_token.type == props.TT_RPAREN:
                result.register(self.advance())
                return result.success(expression)
            else:
                return result.failure(InvalidSyntaxError(
                    self.current_token.pos_start,
                    self.current_token.pos_end,
                    "Expected ')'"
                ))

        return result.failure(InvalidSyntaxError(
            token.pos_start, token.pos_end, 'Expected int or float'
        ))

    def term(self):
        return self.binary_operation(self.factor, (props.TT_MUL, props.TT_DIV))

    def expression(self):
        return self.binary_operation(self.term, (props.TT_PLUS, props.TT_MINUS))

    def binary_operation(self, function, operations):
        result = ParseResult()
        left = result.register(function())
        if result.error:
            return result

        while self.current_token.type in operations:
            op_token = self.current_token
            result.register(self.advance())
            right = result.register(function())
            if result.error:
                return result
            left = BinOpNode(left, op_token, right)
        return result.success(left)


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, result):
        if isinstance(result, ParseResult):
            if result.error:
                self.error = result.error
            return result.node
        return result

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self