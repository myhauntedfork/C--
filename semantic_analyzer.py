class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def define(self, name, var_type):
        if name in self.symbols:
            raise Exception(f"Error: Variable '{name}' already declared.")
        self.symbols[name] = var_type

    def lookup(self, name):
        if name not in self.symbols:
            raise Exception(f"Error: Variable '{name}' not declared.")
        return self.symbols[name]

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit_VarDeclNode(self, node):
        var_name = node.var_name
        var_type = node.var_type
        self.symbol_table.define(var_name, var_type)

    def visit_VarAccessNode(self, node):
        var_name = node.var_name
        var_type = self.symbol_table.lookup(var_name)

    def visit_BinOpNode(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type != right_type:
            raise Exception(f"Type mismatch: {left_type} and {right_type}")

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")
