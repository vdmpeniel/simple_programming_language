from string_with_arrows import string_with_arrows


# Error handling
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        return f'{self.error_name}: {self.details}' + \
            f' File {self.pos_start.filename}, line {self.pos_start.line + 1} column {self.pos_start.column}' + \
            '\n\n' + string_with_arrows(self.pos_start.file_text, self.pos_start, self.pos_end)


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details=None):
        super().__init__(pos_start, pos_end, 'Illegal Character Error', details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=None):
        super().__init__(pos_start, pos_end, 'Invalid Syntax Error', details)
