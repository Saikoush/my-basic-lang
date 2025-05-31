class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def consume(self, expected_type=None, expected_value=None):
        if self.pos < len(self.tokens):
            tok = self.tokens[self.pos]
            if expected_type and tok[0] != expected_type:
                raise Exception(f"Expected token type {expected_type}, got {tok[0]}")
            if expected_value and tok[1] != expected_value:
                raise Exception(f"Expected token value {expected_value}, got {tok[1]}")
            self.pos += 1
            return tok
        raise Exception("Unexpected end of input")

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            statements.append(self.statement())
        return statements

    def statement(self):
        tok = self.peek()
        if tok[0] == 'KEYWORD':
            if tok[1] == 'LET':
                return self.let_statement()
            elif tok[1] == 'PRINT':
                return self.print_statement()
            elif tok[1] == 'IF':
                return self.if_statement()
            elif tok[1] == 'WHILE':
                return self.while_statement()
            elif tok[1] == 'END':
                self.consume('KEYWORD', 'END')
                return ('END',)
        raise Exception(f"Unknown statement: {tok}")

    def let_statement(self):
        self.consume('KEYWORD', 'LET')
        var_name = self.consume('IDENTIFIER')[1]
        self.consume('EQUALS')
        expr = self.expression()
        return ('LET', var_name, expr)

    def print_statement(self):
        self.consume('KEYWORD', 'PRINT')
        expr = self.expression()
        return ('PRINT', expr)

    def if_statement(self):
        self.consume('KEYWORD', 'IF')
        condition = self.condition()
        self.consume('KEYWORD', 'THEN')

        then_body = []
        while self.pos < len(self.tokens) and not (self.peek()[0] == 'KEYWORD' and self.peek()[1] in ('ELSE', 'END')):
            then_body.append(self.statement())

        else_body = []
        if self.pos < len(self.tokens) and self.peek()[0] == 'KEYWORD' and self.peek()[1] == 'ELSE':
            self.consume('KEYWORD', 'ELSE')
            while self.pos < len(self.tokens) and not (self.peek()[0] == 'KEYWORD' and self.peek()[1] == 'END'):
                else_body.append(self.statement())

        self.consume('KEYWORD', 'END')
        return ('IF', condition, then_body, else_body)

    def while_statement(self):
        self.consume('KEYWORD', 'WHILE')
        condition = self.condition()
        self.consume('KEYWORD', 'DO')

        body = []
        while self.pos < len(self.tokens) and not (self.peek()[0] == 'KEYWORD' and self.peek()[1] == 'END'):
            body.append(self.statement())

        self.consume('KEYWORD', 'END')
        return ('WHILE', condition, body)

    def condition(self):
        left = self.expression()
        if self.pos < len(self.tokens) and self.peek()[0] == 'COMPARE':
            op = self.consume('COMPARE')[1]
            right = self.expression()
            return ('CONDITION', op, left, right)
        else:
            raise Exception("Expected comparison operator in condition")

    def expression(self):
        left = self.term()
        while self.pos < len(self.tokens) and self.peek()[0] in ('PLUS', 'MINUS'):
            op = self.consume()[1]
            right = self.term()
            left = ('BIN_OP', op, left, right)
        return left

    def term(self):
        left = self.factor()
        while self.pos < len(self.tokens) and self.peek()[0] in ('MULTIPLY', 'DIVIDE'):
            op = self.consume()[1]
            right = self.factor()
            left = ('BIN_OP', op, left, right)
        return left

    def factor(self):
        tok = self.consume()
        if tok[0] == 'NUMBER':
            return ('NUMBER', tok[1])
        elif tok[0] == 'STRING':
            return ('STRING', tok[1])
        elif tok[0] == 'IDENTIFIER':
            return ('IDENTIFIER', tok[1])
        elif tok[0] == 'LPAREN':
            expr = self.expression()
            self.consume('RPAREN')
            return expr
        else:
            raise Exception(f"Unexpected token in factor: {tok}")
