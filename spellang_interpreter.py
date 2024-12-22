# spelllang_interpreter.py

import sys
import re
from collections import deque

# Define Token Types
TOKEN_TYPES = {
    'KEYWORD': 'KEYWORD',
    'IDENTIFIER': 'IDENTIFIER',
    'NUMBER': 'NUMBER',
    'STRING': 'STRING',
    'OPERATOR': 'OPERATOR',
    'DELIMITER': 'DELIMITER',
    'EOF': 'EOF',
}

# Define Keywords
KEYWORDS = {
    'Wand', 'Incantation', 'Cast', 'Illuminate', 'Ifar', 'Elsear',
    'Loopus', 'Persistus', 'Cauldron', 'SpellBooks', 'Protego',
    'Alohomora', 'Magical', 'Creature', 'Bloodline', 'Forar',
    'in', 'len',
}

# Define Operators
OPERATORS = {
    '=', '==', '!=', '<', '>', '<=', '>=', '+', '-', '*', '/', '%',
    '(', ')', '{', '}', '[', ']', ',', '.', '&&', '||', '!', ':',
}

# Define Patterns
TOKEN_REGEX = [
    ('NUMBER',   r'\d+'),
    ('STRING',   r'\".*?\"'),
    ('IDENTIFIER', r'[A-Za-z_][A-Za-z0-9_]*'),
    ('OPERATOR', r'==|!=|<=|>=|&&|\|\||[=+\-*/%<>!():{},.\[\]]'),
    ('NEWLINE',  r'\n'),
    ('SKIP',     r'[ \t]+'),
    ('MISMATCH', r'.'),
]

# Custom Exceptions
class SpellLangError(Exception):
    pass

class LexerError(SpellLangError):
    def __init__(self, message, line, column):
        super().__init__(f"Lexer Error at line {line}, column {column}: {message}")

class ParserError(SpellLangError):
    def __init__(self, message, token):
        super().__init__(f"Parser Error at line {token.line}, column {token.column}: {message}")

class RuntimeErrorSL(SpellLangError):
    def __init__(self, message, node):
        super().__init__(f"Runtime Error: {message} at line {node.line}, column {node.column}")

# Token Class
class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"{self.type}({self.value}) at {self.line}:{self.column}"

# Lexer Implementation
class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.current_line = 1
        self.current_column = 1
        self.token_regex = [(name, re.compile(pattern)) for name, pattern in TOKEN_REGEX]
    
    def tokenize(self):
        code = self.code
        pos = 0
        while pos < len(code):
            match = None
            for token_type, regex in self.token_regex:
                match = regex.match(code, pos)
                if match:
                    text = match.group(0)
                    if token_type == 'NEWLINE':
                        self.current_line += 1
                        self.current_column = 1
                        pos = match.end()
                        break
                    elif token_type == 'SKIP':
                        pos = match.end()
                        self.current_column += len(text)
                        break
                    elif token_type == 'MISMATCH':
                        raise LexerError(f"Unexpected character '{text}'", self.current_line, self.current_column)
                    else:
                        if token_type == 'IDENTIFIER' and text in KEYWORDS:
                            token = Token('KEYWORD', text, self.current_line, self.current_column)
                        elif token_type == 'IDENTIFIER':
                            token = Token('IDENTIFIER', text, self.current_line, self.current_column)
                        elif token_type == 'NUMBER':
                            token = Token('NUMBER', int(text), self.current_line, self.current_column)
                        elif token_type == 'STRING':
                            token = Token('STRING', text[1:-1], self.current_line, self.current_column)
                        elif token_type == 'OPERATOR':
                            token = Token('OPERATOR', text, self.current_line, self.current_column)
                        else:
                            token = Token(token_type, text, self.current_line, self.current_column)
                        self.tokens.append(token)
                        pos = match.end()
                        self.current_column += len(text)
                        break
            if not match:
                raise LexerError("Invalid syntax", self.current_line, self.current_column)
        self.tokens.append(Token('EOF', None, self.current_line, self.current_column))
        return self.tokens

# AST Node Definitions
class ASTNode:
    def __init__(self, line, column):
        self.line = line
        self.column = column

class Program(ASTNode):
    def __init__(self, statements):
        super().__init__(0, 0)
        self.statements = statements

class VarDeclaration(ASTNode):
    def __init__(self, var_type, name, value, line, column):
        super().__init__(line, column)
        self.var_type = var_type
        self.name = name
        self.value = value

class Assignment(ASTNode):
    def __init__(self, name, value, line, column):
        super().__init__(line, column)
        self.name = name
        self.value = value

class FunctionDeclaration(ASTNode):
    def __init__(self, name, params, body, line, column):
        super().__init__(line, column)
        self.name = name
        self.params = params
        self.body = body

class FunctionCall(ASTNode):
    def __init__(self, name, args, line, column):
        super().__init__(line, column)
        self.name = name
        self.args = args

class IfStatement(ASTNode):
    def __init__(self, condition, if_body, else_body, line, column):
        super().__init__(line, column)
        self.condition = condition
        self.if_body = if_body
        self.else_body = else_body

class WhileLoop(ASTNode):
    def __init__(self, condition, body, line, column):
        super().__init__(line, column)
        self.condition = condition
        self.body = body

class ForLoop(ASTNode):
    def __init__(self, var, iterable, body, line, column):
        super().__init__(line, column)
        self.var = var
        self.iterable = iterable
        self.body = body

class PrintStatement(ASTNode):
    def __init__(self, expression, line, column):
        super().__init__(line, column)
        self.expression = expression

class ClassDeclaration(ASTNode):
    def __init__(self, name, params, body, line, column):
        super().__init__(line, column)
        self.name = name
        self.params = params
        self.body = body

class Inheritance(ASTNode):
    def __init__(self, child, parent, line, column):
        super().__init__(line, column)
        self.child = child
        self.parent = parent

class TryCatch(ASTNode):
    def __init__(self, try_block, catch_block, line, column):
        super().__init__(line, column)
        self.try_block = try_block
        self.catch_block = catch_block

class BinaryOp(ASTNode):
    def __init__(self, left, operator, right, line, column):
        super().__init__(line, column)
        self.left = left
        self.operator = operator
        self.right = right

class UnaryOp(ASTNode):
    def __init__(self, operator, operand, line, column):
        super().__init__(line, column)
        self.operator = operator
        self.operand = operand

class Literal(ASTNode):
    def __init__(self, value, line, column):
        super().__init__(line, column)
        self.value = value

class Identifier(ASTNode):
    def __init__(self, name, line, column):
        super().__init__(line, column)
        self.name = name

# Parser Implementation
class Parser:
    def __init__(self, tokens):
        self.tokens = deque(tokens)
        self.current_token = self.tokens.popleft()
    
    def eat(self, token_type=None, value=None):
        if token_type and self.current_token.type != token_type:
            raise ParserError(f"Expected token type {token_type}, got {self.current_token.type}", self.current_token)
        if value and self.current_token.value != value:
            raise ParserError(f"Expected token value '{value}', got '{self.current_token.value}'", self.current_token)
        self.current_token = self.tokens.popleft()
    
    def parse(self):
        statements = []
        while self.current_token.type != 'EOF':
            stmt = self.statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def statement(self):
        if self.current_token.type == 'KEYWORD':
            if self.current_token.value in {'Wand', 'Cauldron', 'SpellBooks'}:
                return self.variable_declaration()
            elif self.current_token.value == 'Incantation':
                return self.function_declaration()
            elif self.current_token.value == 'Cast':
                return self.function_call_statement()
            elif self.current_token.value == 'Illuminate':
                return self.print_statement()
            elif self.current_token.value == 'Ifar':
                return self.if_statement()
            elif self.current_token.value == 'Loopus':
                return self.for_loop()
            elif self.current_token.value == 'Persistus':
                return self.while_loop()
            elif self.current_token.value == 'Protego':
                return self.try_catch()
            elif self.current_token.value == 'Magical':
                return self.class_declaration()
            else:
                raise ParserError(f"Unknown keyword '{self.current_token.value}'", self.current_token)
        elif self.current_token.type == 'IDENTIFIER':
            return self.assignment()
        else:
            raise ParserError(f"Unexpected token '{self.current_token.value}'", self.current_token)
    
    def variable_declaration(self):
        var_type = self.current_token.value
        line, column = self.current_token.line, self.current_token.column
        self.eat('KEYWORD')
        if self.current_token.type != 'IDENTIFIER':
            raise ParserError("Expected identifier after variable type", self.current_token)
        var_name = self.current_token.value
        self.eat('IDENTIFIER')
        self.eat('OPERATOR', '=')
        value = self.expression()
        self.eat('OPERATOR', '\n') if self.current_token.value == '\n' else None
        return VarDeclaration(var_type, var_name, value, line, column)
    
    def assignment(self):
        var_name = self.current_token.value
        line, column = self.current_token.line, self.current_token.column
        self.eat('IDENTIFIER')
        self.eat('OPERATOR', '=')
        value = self.expression()
        return Assignment(var_name, value, line, column)
    
    def function_declaration(self):
        self.eat('KEYWORD', 'Incantation')
        if self.current_token.type != 'IDENTIFIER':
            raise ParserError("Expected function name after 'Incantation'", self.current_token)
        func_name = self.current_token.value
        line, column = self.current_token.line, self.current_token.column
        self.eat('IDENTIFIER')
        self.eat('OPERATOR', '(')
        params = []
        if self.current_token.type != 'OPERATOR' or self.current_token.value != ')':
            while True:
                if self.current_token.type != 'IDENTIFIER':
                    raise ParserError("Expected parameter name", self.current_token)
                params.append(self.current_token.value)
                self.eat('IDENTIFIER')
                if self.current_token.type == 'OPERATOR' and self.current_token.value == ',':
                    self.eat('OPERATOR', ',')
                else:
                    break
        self.eat('OPERATOR', ')')
        self.eat('OPERATOR', '{')
        body = []
        while not (self.current_token.type == 'OPERATOR' and self.current_token.value == '}'):
            stmt = self.statement()
            if stmt:
                body.append(stmt)
        self.eat('OPERATOR', '}')
        return FunctionDeclaration(func_name, params, body, line, column)
    
    def function_call_statement(self):
        self.eat('KEYWORD', 'Cast')
        if self.current_token.type != 'IDENTIFIER':
            raise ParserError("Expected function name after 'Cast'", self.current_token)
        func_name = self.current_token.value
        line, column = self.current_token.line, self.current_token.column
        self.eat('IDENTIFIER')
        self.eat('OPERATOR', '(')
        args = []
        if self.current_token.type != 'OPERATOR' or self.current_token.value != ')':
            while True:
                arg = self.expression()
                args.append(arg)
                if self.current_token.type == 'OPERATOR' and self.current_token.value == ',':
                    self.eat('OPERATOR', ',')
                else:
                    break
        self.eat('OPERATOR', ')')
        return FunctionCall(func_name, args, line, column)
    
    def print_statement(self):
        self.eat('KEYWORD', 'Illuminate')
        self.eat('OPERATOR', '(')
        expr = self.expression()
        self.eat('OPERATOR', ')')
        return PrintStatement(expr, self.current_token.line, self.current_token.column)
    
    def if_statement(self):
        self.eat('KEYWORD', 'Ifar')
        condition = self.expression()
        self.eat('OPERATOR', '{')
        if_body = []
        while not (self.current_token.type == 'OPERATOR' and self.current_token.value == '}'):
            stmt = self.statement()
            if stmt:
                if_body.append(stmt)
        self.eat('OPERATOR', '}')
        else_body = []
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'Elsear':
            self.eat('KEYWORD', 'Elsear')
            self.eat('OPERATOR', '{')
            while not (self.current_token.type == 'OPERATOR' and self.current_token.value == '}'):
                stmt = self.statement()
                if stmt:
                    else_body.append(stmt)
            self.eat('OPERATOR', '}')
        return IfStatement(condition, if_body, else_body, condition.line, condition.column)
    
    def while_loop(self):
        self.eat('KEYWORD', 'Persistus')
        condition = self.expression()
        self.eat('OPERATOR', '{')
        body = []
        while not (self.current_token.type == 'OPERATOR' and self.current_token.value == '}'):
            stmt = self.statement()
            if stmt:
                body.append(stmt)
        self.eat('OPERATOR', '}')
        return WhileLoop(condition, body, condition.line, condition.column)
    
    def for_loop(self):
        self.eat('KEYWORD', 'Loopus')
        init = self.expression()
        self.eat('OPERATOR', ';')
        condition = self.expression()
        self.eat('OPERATOR', ';')
        increment = self.expression()
        self.eat('OPERATOR', '{')
        body = []
        while not (self.current_token.type == 'OPERATOR' and self.current_token.value == '}'):
            stmt = self.statement()
            if stmt:
                body.append(stmt)
        self.eat('OPERATOR', '}')
        # For simplicity, we'll treat 'Loopus' as a for loop with init, condition, and increment
        # and encapsulate it within WhileLoop during interpretation
        return ForLoop(init, condition, increment, body, init.line, init.column)
    
    def try_catch(self):
        self.eat('KEYWORD', 'Protego')
        self.eat('OPERATOR', '{')
        try_block = []
        while not (self.current_token.type == 'OPERATOR' and self.current_token.value == '}'):
            stmt = self.statement()
            if stmt:
                try_block.append(stmt)
        self.eat('OPERATOR', '}')
        self.eat('KEYWORD', 'Alohomora')
        self.eat('OPERATOR', '{')
        catch_block = []
        while not (self.current_token.type == 'OPERATOR' and self.current_token.value == '}'):
            stmt = self.statement()
            if stmt:
                catch_block.append(stmt)
        self.eat('OPERATOR', '}')
        return TryCatch(try_block, catch_block, try_block[0].line if try_block else 0, try_block[0].column if try_block else 0)
    
    def class_declaration(self):
        self.eat('KEYWORD', 'Magical')
        self.eat('KEYWORD', 'Creature')
        if self.current_token.type != 'IDENTIFIER':
            raise ParserError("Expected class name after 'Magical Creature'", self.current_token)
        class_name = self.current_token.value
        line, column = self.current_token.line, self.current_token.column
        self.eat('IDENTIFIER')
        self.eat('OPERATOR', '(')
        params = []
        if self.current_token.type != 'OPERATOR' or self.current_token.value != ')':
            while True:
                if self.current_token.type != 'IDENTIFIER':
                    raise ParserError("Expected parameter name", self.current_token)
                params.append(self.current_token.value)
                self.eat('IDENTIFIER')
                if self.current_token.type == 'OPERATOR' and self.current_token.value == ',':
                    self.eat('OPERATOR', ',')
                else:
                    break
        self.eat('OPERATOR', ')')
        inheritance = None
        if self.current_token.type == 'KEYWORD' and self.current_token.value == 'Bloodline':
            self.eat('KEYWORD', 'Bloodline')
            if self.current_token.type != 'IDENTIFIER':
                raise ParserError("Expected parent class name after 'Bloodline'", self.current_token)
            inheritance = self.current_token.value
            self.eat('IDENTIFIER')
        self.eat('OPERATOR', '{')
        body = []
        while not (self.current_token.type == 'OPERATOR' and self.current_token.value == '}'):
            stmt = self.statement()
            if stmt:
                body.append(stmt)
        self.eat('OPERATOR', '}')
        return ClassDeclaration(class_name, params, body, line, column) if not inheritance else Inheritance(class_name, inheritance, line, column)
    
    def expression(self):
        return self.logical_or()
    
    def logical_or(self):
        node = self.logical_and()
        while self.current_token.type == 'OPERATOR' and self.current_token.value == '||':
            op = self.current_token.value
            line, column = self.current_token.line, self.current_token.column
            self.eat('OPERATOR', '||')
            right = self.logical_and()
            node = BinaryOp(node, op, right, line, column)
        return node
    
    def logical_and(self):
        node = self.equality()
        while self.current_token.type == 'OPERATOR' and self.current_token.value == '&&':
            op = self.current_token.value
            line, column = self.current_token.line, self.current_token.column
            self.eat('OPERATOR', '&&')
            right = self.equality()
            node = BinaryOp(node, op, right, line, column)
        return node
    
    def equality(self):
        node = self.comparison()
        while self.current_token.type == 'OPERATOR' and self.current_token.value in {'==', '!='}:
            op = self.current_token.value
            line, column = self.current_token.line, self.current_token.column
            self.eat('OPERATOR', op)
            right = self.comparison()
            node = BinaryOp(node, op, right, line, column)
        return node
    
    def comparison(self):
        node = self.term()
        while self.current_token.type == 'OPERATOR' and self.current_token.value in {'<', '>', '<=', '>='}:
            op = self.current_token.value
            line, column = self.current_token.line, self.current_token.column
            self.eat('OPERATOR', op)
            right = self.term()
            node = BinaryOp(node, op, right, line, column)
        return node
    
    def term(self):
        node = self.factor()
        while self.current_token.type == 'OPERATOR' and self.current_token.value in {'+', '-'}:
            op = self.current_token.value
            line, column = self.current_token.line, self.current_token.column
            self.eat('OPERATOR', op)
            right = self.factor()
            node = BinaryOp(node, op, right, line, column)
        return node
    
    def factor(self):
        node = self.unary()
        while self.current_token.type == 'OPERATOR' and self.current_token.value in {'*', '/', '%'}:
            op = self.current_token.value
            line, column = self.current_token.line, self.current_token.column
            self.eat('OPERATOR', op)
            right = self.unary()
            node = BinaryOp(node, op, right, line, column)
        return node
    
    def unary(self):
        if self.current_token.type == 'OPERATOR' and self.current_token.value in {'!', '-'}:
            op = self.current_token.value
            line, column = self.current_token.line, self.current_token.column
            self.eat('OPERATOR', op)
            operand = self.unary()
            return UnaryOp(op, operand, line, column)
        return self.primary()
    
    def primary(self):
        token = self.current_token
        if token.type == 'NUMBER':
            self.eat('NUMBER')
            return Literal(token.value, token.line, token.column)
        elif token.type == 'STRING':
            self.eat('STRING')
            return Literal(token.value, token.line, token.column)
        elif token.type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            if self.current_token.type == 'OPERATOR' and self.current_token.value == '(':
                # Function call within expression
                self.eat('OPERATOR', '(')
                args = []
                if self.current_token.type != 'OPERATOR' or self.current_token.value != ')':
                    while True:
                        arg = self.expression()
                        args.append(arg)
                        if self.current_token.type == 'OPERATOR' and self.current_token.value == ',':
                            self.eat('OPERATOR', ',')
                        else:
                            break
                self.eat('OPERATOR', ')')
                return FunctionCall(token.value, args, token.line, token.column)
            return Identifier(token.value, token.line, token.column)
        elif token.type == 'OPERATOR' and token.value == '(':
            self.eat('OPERATOR', '(')
            expr = self.expression()
            self.eat('OPERATOR', ')')
            return expr
        elif token.type == 'OPERATOR' and token.value == '[':
            return self.list_expression()
        elif token.type == 'OPERATOR' and token.value == '{':
            return self.dict_expression()
        else:
            raise ParserError(f"Unexpected token '{token.value}' in expression", token)
    
    def list_expression(self):
        line, column = self.current_token.line, self.current_token.column
        self.eat('OPERATOR', '[')
        items = []
        if self.current_token.type != 'OPERATOR' or self.current_token.value != ']':
            while True:
                item = self.expression()
                items.append(item)
                if self.current_token.type == 'OPERATOR' and self.current_token.value == ',':
                    self.eat('OPERATOR', ',')
                else:
                    break
        self.eat('OPERATOR', ']')
        return Literal(items, line, column)
    
    def dict_expression(self):
        line, column = self.current_token.line, self.current_token.column
        self.eat('OPERATOR', '{')
        items = {}
        if self.current_token.type != 'OPERATOR' or self.current_token.value != '}':
            while True:
                key = self.expression()
                self.eat('OPERATOR', ':')
                value = self.expression()
                items[key] = value
                if self.current_token.type == 'OPERATOR' and self.current_token.value == ',':
                    self.eat('OPERATOR', ',')
                else:
                    break
        self.eat('OPERATOR', '}')
        return Literal(items, line, column)

# Environment and Interpreter
class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent
    
    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise RuntimeErrorSL(f"Variable '{name}' is not defined.", None)
    
    def set(self, name, value):
        self.vars[name] = value
    
    def update(self, name, value):
        if name in self.vars:
            self.vars[name] = value
        elif self.parent:
            self.parent.update(name, value)
        else:
            raise RuntimeErrorSL(f"Variable '{name}' is not defined.", None)

class Function:
    def __init__(self, name, params, body, closure):
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure
    
    def call(self, interpreter, args):
        if len(args) != len(self.params):
            raise RuntimeErrorSL(f"Function '{self.name}' expects {len(self.params)} arguments, got {len(args)}.", self.body[0])
        env = Environment(self.closure)
        for param, arg in zip(self.params, args):
            env.set(param, arg)
        return interpreter.execute_block(self.body, env)

class Class:
    def __init__(self, name, params, body, closure, parent=None):
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure
        self.parent = parent
        self.methods = {}
        self.attributes = {}
    
    def call(self, interpreter, args):
        if len(args) != len(self.params):
            raise RuntimeErrorSL(f"Class '{self.name}' expects {len(self.params)} arguments, got {len(args)}.", self.body[0])
        instance = Instance(self)
        env = Environment(self.closure)
        for param, arg in zip(self.params, args):
            env.set(param, arg)
        interpreter.execute_block(self.body, env, instance)
        return instance

class Instance:
    def __init__(self, cls):
        self.cls = cls
        self.fields = {}
    
    def get(self, name):
        if name in self.fields:
            return self.fields[name]
        elif name in self.cls.methods:
            return self.cls.methods[name]
        else:
            raise RuntimeErrorSL(f"Attribute or method '{name}' not found in class '{self.cls.name}'.", None)
    
    def set(self, name, value):
        self.fields[name] = value

class Interpreter:
    def __init__(self, tree):
        self.tree = tree
        self.global_env = Environment()
        self.env = self.global_env
        self.functions = {}
        self.classes = {}
        self.setup_builtins()
    
    def setup_builtins(self):
        # Define built-in functions (spells)
        self.global_env.set('len', len)
        self.global_env.set('str', str)
        self.global_env.set('int', int)
    
    def interpret(self):
        try:
            for stmt in self.tree.statements:
                self.execute(stmt)
        except SpellLangError as e:
            print(e)
    
    def execute(self, node):
        method_name = f'execute_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_execute)
        return method(node)
    
    def generic_execute(self, node):
        raise RuntimeErrorSL(f"No execute_{type(node).__name__} method", node)
    
    def execute_Program(self, node):
        for stmt in node.statements:
            self.execute(stmt)
    
    def execute_VarDeclaration(self, node):
        value = self.evaluate(node.value)
        self.env.set(node.name, value)
    
    def execute_Assignment(self, node):
        value = self.evaluate(node.value)
        self.env.update(node.name, value)
    
    def execute_FunctionDeclaration(self, node):
        func = Function(node.name, node.params, node.body, self.env)
        self.functions[node.name] = func
        self.env.set(node.name, func)
    
    def execute_FunctionCall(self, node):
        func = self.env.get(node.name)
        if isinstance(func, Function):
            args = [self.evaluate(arg) for arg in node.args]
            return func.call(self, args)
        elif callable(func):
            args = [self.evaluate(arg) for arg in node.args]
            return func(*args)
        elif isinstance(func, Instance):
            # Handle method calls if needed
            pass
        else:
            raise RuntimeErrorSL(f"'{node.name}' is not a function", node)
    
    def execute_PrintStatement(self, node):
        value = self.evaluate(node.expression)
        print(value)
    
    def execute_IfStatement(self, node):
        condition = self.evaluate(node.condition)
        if self.is_truthy(condition):
            self.execute_block(node.if_body, Environment(self.env))
        else:
            self.execute_block(node.else_body, Environment(self.env))
    
    def execute_WhileLoop(self, node):
        while self.is_truthy(self.evaluate(node.condition)):
            self.execute_block(node.body, Environment(self.env))
    
    def execute_ForLoop(self, node):
        # Execute initialization
        self.execute(node.var)
        while self.is_truthy(self.evaluate(node.condition)):
            self.execute_block(node.body, Environment(self.env))
            # Execute increment
            self.execute(node.increment)
    
    def execute_ClassDeclaration(self, node):
        cls = Class(node.name, node.params, node.body, self.env)
        self.classes[node.name] = cls
        self.env.set(node.name, cls)
    
    def execute_Inheritance(self, node):
        if node.parent not in self.classes:
            raise RuntimeErrorSL(f"Parent class '{node.parent}' not found.", node)
        parent_cls = self.classes[node.parent]
        cls = Class(node.child, [], [], self.env, parent=parent_cls)
        self.classes[node.child] = cls
        self.env.set(node.child, cls)
    
    def execute_TryCatch(self, node):
        try:
            self.execute_block(node.try_block, Environment(self.env))
        except SpellLangError as e:
            self.execute_block(node.catch_block, Environment(self.env))
    
    def execute_block(self, statements, env, instance=None):
        previous_env = self.env
        self.env = env
        if instance:
            self.env.set('self', instance)
        try:
            for stmt in statements:
                self.execute(stmt)
        finally:
            self.env = previous_env
    
    def evaluate(self, node):
        method_name = f'evaluate_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_evaluate)
        return method(node)
    
    def generic_evaluate(self, node):
        raise RuntimeErrorSL(f"No evaluate_{type(node).__name__} method", node)
    
    def evaluate_Literal(self, node):
        if isinstance(node.value, list):
            return [self.evaluate(item) for item in node.value]
        elif isinstance(node.value, dict):
            return {self.evaluate(k): self.evaluate(v) for k, v in node.value.items()}
        else:
            return node.value
    
    def evaluate_Identifier(self, node):
        return self.env.get(node.name)
    
    def evaluate_BinaryOp(self, node):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        op = node.operator
        try:
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                return left / right
            elif op == '%':
                return left % right
            elif op == '==':
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
            elif op == '&&':
                return self.is_truthy(left) and self.is_truthy(right)
            elif op == '||':
                return self.is_truthy(left) or self.is_truthy(right)
            else:
                raise RuntimeErrorSL(f"Unknown operator '{op}'", node)
        except Exception as e:
            raise RuntimeErrorSL(str(e), node)
    
    def evaluate_UnaryOp(self, node):
        operand = self.evaluate(node.operand)
        op = node.operator
        try:
            if op == '-':
                return -operand
            elif op == '!':
                return not self.is_truthy(operand)
            else:
                raise RuntimeErrorSL(f"Unknown unary operator '{op}'", node)
        except Exception as e:
            raise RuntimeErrorSL(str(e), node)
    
    def evaluate_FunctionCall(self, node):
        return self.execute_FunctionCall(node)
    
    def evaluate_FunctionCall(self, node):
        func = self.env.get(node.name)
        if isinstance(func, Function):
            args = [self.evaluate(arg) for arg in node.args]
            return func.call(self, args)
        elif callable(func):
            args = [self.evaluate(arg) for arg in node.args]
            try:
                return func(*args)
            except Exception as e:
                raise RuntimeErrorSL(str(e), node)
        elif isinstance(func, Class):
            args = [self.evaluate(arg) for arg in node.args]
            return func.call(self, args)
        elif isinstance(func, Instance):
            # Handle instance method calls if needed
            pass
        else:
            raise RuntimeErrorSL(f"'{node.name}' is not a function or class", node)
    
    def is_truthy(self, value):
        return bool(value)
    
    def evaluate_ListAccess(self, node):
        # To be implemented for accessing list elements
        pass
    
    def evaluate_DictAccess(self, node):
        # To be implemented for accessing dictionary elements
        pass

# Main Execution
def main():
    if len(sys.argv) != 2:
        print("Usage: python spelllang_interpreter.py <filename.spell>")
        sys.exit(1)
    
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        sys.exit(1)
    
    # Lexing
    lexer = Lexer(code)
    try:
        tokens = lexer.tokenize()
    except LexerError as e:
        print(e)
        sys.exit(1)
    
    # Parsing
    parser = Parser(tokens)
    try:
        tree = parser.parse()
    except ParserError as e:
        print(e)
        sys.exit(1)
    
    # Interpreting
    interpreter = Interpreter(tree)
    interpreter.interpret()

if __name__ == "__main__":
    main()
