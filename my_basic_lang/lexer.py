class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos < len(self.text):
            return self.text[peek_pos]
        return None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        dot_count = 0
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
            result += self.current_char
            self.advance()
        if dot_count == 0:
            return ('NUMBER', int(result))
        else:
            return ('NUMBER', float(result))

    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        if result.upper() in ('LET', 'PRINT', 'IF', 'THEN', 'ELSE', 'WHILE', 'DO', 'END'):
            return ('KEYWORD', result.upper())
        return ('IDENTIFIER', result)

    def string(self):
        quote_char = self.current_char  # can be ' or "
        self.advance()  # skip opening quote
        result = ''
        while self.current_char is not None and self.current_char != quote_char:
            result += self.current_char
            self.advance()
        if self.current_char != quote_char:
            raise Exception("Unterminated string literal")
        self.advance()  # skip closing quote
        return ('STRING', result)

    def generate_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                tokens.append(self.number())
                continue

            if self.current_char.isalpha():
                tokens.append(self.identifier())
                continue
            if self.current_char == ',':
                 tokens.append(('COMMA', ','))
                 self.advance()
                 continue

            if self.current_char in ('"', "'"):
                tokens.append(self.string())
                continue

            # Multi-char comparison operators
            if self.current_char == '=':
                next_char = self.peek()
                if next_char == '=':
                    self.advance()
                    self.advance()
                    tokens.append(('COMPARE', '=='))
                else:
                    self.advance()
                    tokens.append(('EQUALS', '='))
                continue
                if self.current_char == ',':
                 tokens.append(('COMMA', ','))
                 self.advance()
                 continue

            if self.current_char == '!':
                next_char = self.peek()
                if next_char == '=':
                    self.advance()
                    self.advance()
                    tokens.append(('COMPARE', '!='))
                else:
                    raise Exception("Unexpected character '!'")
                continue

            if self.current_char == '<':
                next_char = self.peek()
                if next_char == '=':
                    self.advance()
                    self.advance()
                    tokens.append(('COMPARE', '<='))
                else:
                    self.advance()
                    tokens.append(('COMPARE', '<'))
                continue

            if self.current_char == '>':
                next_char = self.peek()
                if next_char == '=':
                    self.advance()
                    self.advance()
                    tokens.append(('COMPARE', '>='))
                else:
                    self.advance()
                    tokens.append(('COMPARE', '>'))
                continue

            if self.current_char == '+':
                tokens.append(('PLUS', '+'))
                self.advance()
                continue

            if self.current_char == '-':
                tokens.append(('MINUS', '-'))
                self.advance()
                continue

            if self.current_char == '*':
                tokens.append(('MULTIPLY', '*'))
                self.advance()
                continue

            if self.current_char == '/':
                tokens.append(('DIVIDE', '/'))
                self.advance()
                continue

            if self.current_char == '(':
                tokens.append(('LPAREN', '('))
                self.advance()
                continue

            if self.current_char == ')':
                tokens.append(('RPAREN', ')'))
                self.advance()
                continue

            raise Exception(f"Unexpected character {self.current_char}")

        return tokens
