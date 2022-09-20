from lexer import Lexer
from parser import Parser


def main_loop():
    while True:
        text = input('basic > ')
        result, error = run('<stdin>', text)
        if error:
            print(error.as_string())
        else:
            print(result)


def run(filename, text):
    # Generate tokens
    lexer = Lexer(filename, text)
    tokens, error = lexer.tokenize()
    if error:
        return None, error

    # Generate AST (Abstract syntax tree)
    parser = Parser(tokens)
    ast = parser.parse()
    return ast.node, ast.error




