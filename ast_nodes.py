class NumberNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'NumberNode({self.value})'

class StringNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'StringNode("{self.value}")'

class VarAccessNode:
    def __init__(self, var_name):
        self.var_name = var_name

    def __repr__(self):
        return f'VarAccessNode({self.var_name})'

class VarAssignNode:
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

    def __repr__(self):
        return f'VarAssignNode({self.var_name}, {self.value})'

class BinOpNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f'BinOpNode({self.left}, {self.operator}, {self.right})'

class PrintNode:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f'PrintNode({self.expression})'

class IfNode:
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

    def __repr__(self):
        return f'IfNode({self.condition}, {self.then_body}, {self.else_body})'

class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f'WhileNode({self.condition}, {self.body})'
