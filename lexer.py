import properties as props
from token import Token
from error_handling import *


# LEXER
class Lexer:
    def __init__(self, filename, text):
        self.filename = filename
        self.text = text
        self.pos = Position(-1, 0, -1, filename, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def tokenize(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(props.TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(props.TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(props.TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(props.TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(props.TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(props.TT_RPAREN))
                self.advance()
            elif self.current_char in props.DIGITS:
                tokens.append(self.make_number())
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}'")

        tokens.append(Token(props.TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char is not None \
                and self.current_char in (props.DIGITS + '.'):
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
            num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(props.TT_INT, int(num_str), pos_start, self.pos)
        return Token(props.TT_FLOAT, float(num_str), pos_start, self.pos)


class Position:
    def __init__(self, index, line, column, filename, file_text):
        self.index = index
        self.line = line
        self.column = column
        self.filename = filename
        self.file_text = file_text

    def advance(self, current_char=None):
        self.index += 1
        self.column += 1
        if current_char == '\n':
            self.line += 1
            self.column = 0
        return self

    def copy(self):
        return Position(self.index, self.line, self.column, self.filename, self.file_text)



