# Error handling
class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details

    def as_string(self):
        return f'{self.error_name}: {self.details}'


class IllegalCharError(Error):
    def __init__(self, details=None):
        super().__init__('Illegal Character Error', details)


# Token Types:
TT_INT = 'int'
TT_FLOAT = 'float'
TT_PLUS = 'plus'
TT_MINUS = 'minus'
TT_MUL = 'multiplication'
TT_DIV = 'division'
TT_LPAREN = 'l_parent'
TT_RPAREN = 'r_parent'
DIGITS = '1234567890'


class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'




# LEXER
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def tokenize(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            else:
                char = self.current_char
                self.advance()
                return [], IllegalCharError(f"'{char}'")

        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        while self.current_char is not None \
                and self.current_char in (DIGITS + '.'):
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
            num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str))
        return Token(TT_FLOAT, float(num_str))


def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.tokenize()
    return tokens, error
