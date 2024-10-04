class CodeGenerator:
    def __init__(self):
        self.output = []

    def generate(self, node):
        if isinstance(node, list):
            for sub_node in node:
                self.visit(sub_node)
        else:
            self.visit(node)

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")

    def visit_NumberNode(self, node):
        return str(node.value)

    def visit_StringNode(self, node):
        return f'"{node.value}"'

    def visit_BinOpNode(self, node):
        left_code = self.visit(node.left)
        right_code = self.visit(node.right)
        operator = node.operator
        return f'({left_code} {operator} {right_code})'

    def visit_VarAssignNode(self, node):
        var_name = node.var_name
        value_code = self.visit(node.value)
        return f'{var_name} = {value_code}'

    def visit_VarAccessNode(self, node):
        return node.var_name

    def visit_PrintNode(self, node):
        expr_code = self.visit(node.expression)
        return f'print({expr_code})'

    def visit_IfNode(self, node):
        condition_code = self.visit(node.condition)
        then_code = '\n'.join([self.visit(stmt) for stmt in node.then_body])
        code = f'if ({condition_code}):\n    {then_code}'
        if node.else_body:
            else_code = '\n'.join([self.visit(stmt) for stmt in node.else_body])
            code += f'\nelse:\n    {else_code}'
        return code

    def visit_WhileNode(self, node):
        condition_code = self.visit(node.condition)
        body_code = '\n'.join([self.visit(stmt) for stmt in node.body])
        return f'while ({condition_code}):\n    {body_code}'
