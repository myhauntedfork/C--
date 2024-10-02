class SemanticError(Exception):
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(f"SemanticError: {message} at line {self.line}, column {self.column}")

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name, value_type, line, column):
        if name in self.symbols:
            raise SemanticError(f"Variable '{name}' already declared", line, column)
        self.symbols[name] = value_type

    def lookup(self, name, line, column):
        if name not in self.symbols:
            raise SemanticError(f"Variable '{name}' not declared", line, column)
        return self.symbols[name]

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def analyze(self, node):
        if isinstance(node, VarAssignNode):
            self.analyze_var_assign(node)
        elif isinstance(node, VarAccessNode):
            self.analyze_var_access(node)
        elif isinstance(node, IfNode):
            self.analyze_if(node)
        elif isinstance(node, WhileNode):
            self.analyze_while(node)
        elif isinstance(node, PrintNode):
            self.analyze(node.expression)
        elif isinstance(node, BinOpNode):
            self.analyze_binop(node)
        elif isinstance(node, NumberNode):
            pass
        else:
            raise SemanticError(f"Unknown node type {type(node).__name__}", 0, 0)

    def analyze_var_assign(self, node):
        self.symbol_table.declare(node.var_name, "number", node.line, node.column)
        self.analyze(node.value)

    def analyze_var_access(self, node):
        self.symbol_table.lookup(node.var_name, node.line, node.column)

    def analyze_if(self, node):
        self.analyze(node.condition)
        for statement in node.then_body:
            self.analyze(statement)
        if node.else_body:
            for statement in node.else_body:
                self.analyze(statement)

    def analyze_while(self, node):
        self.analyze(node.condition)
        for statement in node.body:
            self.analyze(statement)

    def analyze_binop(self, node):
        self.analyze(node.left)
        self.analyze(node.right)
        # Further type checking could be added here
