import re

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line: {self.line}, column: {self.column})"

class LexerError(Exception):
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f'LexerError: {message} at line {line}, column {column}')

class Lexer:
    TOKEN_SPECIFICATION = [
        ('KEYWORD', r'\b(print|noCap|Cap|if|else if|else|while)\b'),
        ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('NUMBER', r'\d+(\.\d+)?([eE][-+]?\d+)?'),
        ('STRING', r'"[^"]*"'),
        ('OPERATOR', r'==|!=|&&|\|\||[+\-*/=><!]'),
        ('DELIMITER', r'[\(\)\[\]\{\};,]'),
        ('COMMENT', r'//.*|/\*[\s\S]*?\*/'),
        ('WHITESPACE', r'\s+'),
    ]

    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.current_position = 0
        self.line = 1
        self.column = 1

        self.token_re = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.TOKEN_SPECIFICATION)

    def tokenize(self):
        for match in re.finditer(self.token_re, self.code):
            kind = match.lastgroup
            value = match.group(kind)

            if kind == 'WHITESPACE' or kind == 'COMMENT':
                self.update_position(match)
                continue

            token = Token(kind, value, self.line, self.column)
            self.tokens.append(token)

            self.update_position(match)

        if self.current_position != len(self.code):
            unrecognized_char = self.code[self.current_position]
            raise LexerError(f"Unrecognized character '{unrecognized_char}'", self.line, self.column)

        return self.tokens

    def update_position(self, match):
        start, end = match.span()
        text = match.group(0)

        lines = text.splitlines()
        if len(lines) > 1:
            self.line += len(lines) - 1
            self.column = len(lines[-1]) + 1
        else:
            self.column += end - start

        self.current_position = end

    def error(self, message):
        raise LexerError(message, self.line, self.column)
