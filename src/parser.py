from semantic_analyzer import SemanticAnalyzer
from code_generator import CodeGenerator
from ast_nodes import (
    NumberNode, StringNode, VarAccessNode, VarAssignNode, 
    BinOpNode, PrintNode, IfNode, WhileNode
)

class ParserError(Exception):
    def __init__(self, message, token):
        self.message = message
        self.line = token.line if token else 'EOF'
        self.column = token.column if token else 'EOF'
        self.token = token
        super().__init__(f'ParserError: {message} at line {self.line}, column {self.column}')

class Parser:
    PRECEDENCE = {
        '||': 1,
        '&&': 2,
        '==': 3, '!=': 3,
        '>': 4, '<': 4, '>=': 4, '<=': 4,
        '+': 5, '-': 5,
        '*': 6, '/': 6,
    }

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]
        self.semantic_analyzer = SemanticAnalyzer()
        self.code_generator = CodeGenerator()

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
            raise ParserError(f"Expected {token_type}, got {self.current_token.type if self.current_token else 'EOF'}", self.current_token)

    def parse(self):
        statements = []
        while self.current_token:
            statement = self.parse_statement()
            if statement:
                statements.append(statement)
        
        for statement in statements:
            self.semantic_analyzer.visit(statement)
        
        generated_code = self.code_generator.generate(statements)
        return generated_code

    def parse_statement(self):
        if self.current_token.type == 'KEYWORD':
            if self.current_token.value == 'if':
                return self.parse_if_statement()
            elif self.current_token.value == 'while':
                return self.parse_while_statement()
            elif self.current_token.value == 'print':
                return self.parse_print_statement()
            else:
                raise ParserError(f"Unexpected keyword '{self.current_token.value}'", self.current_token)
        elif self.current_token.type == 'IDENTIFIER':
            return self.parse_assignment()
        else:
            raise ParserError(f"Unexpected token '{self.current_token}'", self.current_token)

    def parse_block(self):
        statements = []
        self.expect('DELIMITER')
        while self.current_token and self.current_token.value != '}':
            statements.append(self.parse_statement())
        self.expect('DELIMITER')
        return statements

    def parse_if_statement(self):
        self.expect('KEYWORD')
        condition = self.parse_expression()
        self.expect('DELIMITER')
        then_body = self.parse_block()

        else_body = None
        if self.current_token and self.current_token.value == 'else':
            self.advance()
            if self.current_token and self.current_token.value == 'if':
                else_body = [self.parse_if_statement()]
            else:
                self.expect('DELIMITER')
                else_body = self.parse_block()

        return IfNode(condition, then_body, else_body)

    def parse_while_statement(self):
        self.expect('KEYWORD')
        condition = self.parse_expression()
        self.expect('DELIMITER')
        body = self.parse_block()
        return WhileNode(condition, body)

    def parse_assignment(self):
        var_name = self.current_token.value
        self.expect('IDENTIFIER')
        self.expect('OPERATOR')
        value = self.parse_expression()
        return VarAssignNode(var_name, value)

    def parse_print_statement(self):
        self.expect('KEYWORD')
        self.expect('DELIMITER')
        expression = self.parse_expression()
        self.expect('DELIMITER')
        return PrintNode(expression)

    def parse_expression(self, precedence=0):
        left = self.parse_term()

        while self.current_token and self.current_token.type == 'OPERATOR':
            operator = self.current_token.value
            operator_precedence = self.PRECEDENCE.get(operator, 0)

            if operator_precedence < precedence:
                break

            self.advance()
            right = self.parse_expression(operator_precedence + 1)
            left = BinOpNode(left, operator, right)

        return left

    def parse_term(self):
        if self.current_token.type == 'NUMBER':
            value = self.current_token.value
            self.advance()
            return NumberNode(value)
        elif self.current_token.type == 'STRING':
            value = self.current_token.value
            self.advance()
            return StringNode(value)
        elif self.current_token.type == 'IDENTIFIER':
            var_name = self.current_token.value
            self.advance()
            return VarAccessNode(var_name)
        elif self.current_token.value == 'Cap':
            self.advance()
            return NumberNode(1)
        elif self.current_token.value == 'noCap':
            self.advance()
            return NumberNode(0)
        else:
            raise ParserError(f"Unexpected token '{self.current_token}'", self.current_token)
