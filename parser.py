class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def expect(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Expected {token_type}, got {self.current_token.type}")

    def parse(self):
        statements = []
        while self.current_token:
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        return statements

    def parse_statement(self):
        if self.current_token.type == 'KEYWORD':
            if self.current_token.value == 'if':
                statement = self.parse_if_statement()
            elif self.current_token.value == 'while':
                statement = self.parse_while_statement()
            elif self.current_token.value == 'print':
                statement = self.parse_print_statement()
            else:
                raise SyntaxError(f"Unexpected keyword {self.current_token.value}")
        elif self.current_token.type == 'IDENTIFIER':
            statement = self.parse_assignment()
        else:
            raise SyntaxError(f"Unexpected token {self.current_token}")

        if self.current_token and self.current_token.type == 'DELIMITER' and self.current_token.value == ';':
            self.advance()
        return statement

    def parse_if_statement(self):
        self.expect('KEYWORD')
        condition = self.parse_expression()
        self.expect('DELIMITER')
        then_body = []
        while self.current_token and self.current_token.value != '}':
            then_body.append(self.parse_statement())
        self.expect('DELIMITER')
        else_body = None
        if self.current_token and self.current_token.value == 'else':
            self.advance()
            if self.current_token and self.current_token.value == 'if':
                else_body = [self.parse_if_statement()]
            else:
                self.expect('DELIMITER')
                else_body = []
                while self.current_token and self.current_token.value != '}':
                    else_body.append(self.parse_statement())
                self.expect('DELIMITER')
        return IfNode(condition, then_body, else_body)

    def parse_while_statement(self):
        self.expect('KEYWORD')
        condition = self.parse_expression()
        self.expect('DELIMITER')
        body = []
        while self.current_token and self.current_token.value != '}':
            body.append(self.parse_statement())
        self.expect('DELIMITER')
        return WhileNode(condition, body)

    def parse_assignment(self):
        var_name = self.current_token.value
        self.expect('IDENTIFIER')
        self.expect('OPERATOR')
        value = self.parse_expression()
        return VarAssignNode(var_name, value)

    def parse_print_statement(self):
        self.expect('KEYWORD')
        self.expect('DELIMITER')  # For the opening parenthesis
        expression = self.parse_expression()
        self.expect('DELIMITER')  # For the closing parenthesis
        return PrintNode(expression)

    def parse_expression(self):
        left = self.parse_term()
        while self.current_token and self.current_token.type == 'OPERATOR':
            operator = self.current_token.value
            self.advance()
            right = self.parse_term()
            left = BinOpNode(left, operator, right)
        return left

    def parse_term(self):
        if self.current_token.type == 'NUMBER':
            value = self.current_token.value
            self.advance()
            return NumberNode(value)
        elif self.current_token.type == 'IDENTIFIER':
            var_name = self.current_token.value
            self.advance()
            return VarAccessNode(var_name)
        elif self.current_token.value == 'Cap':  # True
            self.advance()
            return NumberNode(1)  # True as 1
        elif self.current_token.value == 'noCap':  # False
            self.advance()
            return NumberNode(0)  # False as 0
        else:
            raise SyntaxError(f"Unexpected token {self.current_token}")
