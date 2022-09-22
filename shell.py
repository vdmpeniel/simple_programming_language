from lexer import Lexer
from parser import Parser
from interpreter import Interpreter, Context


def main_loop():
    while True:
        text = input('basic > ')
        rt_result, error = run('<stdin>', text)
        if error:
            print(error.as_string())
        else:
            print(rt_result.value)


def run(filename, text):
    # Generate tokens
    lexer = Lexer(filename, text)
    tokens, error = lexer.tokenize()
    if error:
        return None, error

    # Generate AST (Abstract syntax tree)
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    # Run program
    interpreter = Interpreter()
    context = Context('<Program>')
    rt_result = interpreter.visit(ast.node, context)
    return rt_result.value, rt_result.error











