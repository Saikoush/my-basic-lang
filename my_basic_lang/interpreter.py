class Interpreter:
    def __init__(self):
        self.env = {}
        self.output = []

    def interpret(self, statements):
        self.output = []
        for stmt in statements:
            self.visit(stmt)
        return "\n".join(self.output)

    def visit(self, node):
        nodetype = node[0]

        if nodetype == 'LET':
            _, var_name, expr = node
            value = self.eval_expr(expr)
            self.env[var_name] = value

        elif nodetype == 'PRINT':
            _, expr = node
            value = self.eval_expr(expr)
            self.output.append(str(value))

        elif nodetype == 'IF':
            _, condition, then_body, else_body = node
            if self.eval_condition(condition):
                for stmt in then_body:
                    self.visit(stmt)
            else:
                for stmt in else_body:
                    self.visit(stmt)

        elif nodetype == 'WHILE':
            _, condition, body = node
            while self.eval_condition(condition):
                for stmt in body:
                    self.visit(stmt)

        elif nodetype == 'END':
            # just a marker, do nothing
            pass

        else:
            raise Exception(f"Unknown node type {nodetype}")

    def eval_condition(self, node):
        # node = ('CONDITION', op, left, right)
        _, op, left_node, right_node = node
        left = self.eval_expr(left_node)
        right = self.eval_expr(right_node)

        if op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
        else:
            raise Exception(f"Unknown comparison operator {op}")

    def eval_expr(self, node):
        nodetype = node[0]

        if nodetype == 'NUMBER':
            return node[1]

        elif nodetype == 'STRING':
            return node[1]

        elif nodetype == 'IDENTIFIER':
            var_name = node[1]
            if var_name in self.env:
                return self.env[var_name]
            else:
                raise Exception(f"Undefined variable '{var_name}'")

        elif nodetype == 'BIN_OP':
            _, op, left_node, right_node = node
            left = self.eval_expr(left_node)
            right = self.eval_expr(right_node)

            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                if right == 0:
                    raise Exception("Division by zero")
                return left / right
            else:
                raise Exception(f"Unknown operator {op}")

        else:
            raise Exception(f"Unknown expression node {nodetype}")
