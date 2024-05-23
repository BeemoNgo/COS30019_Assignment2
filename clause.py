from propositionalSymbol import PropositionalSymbol
import re
import sympy
from sympy import And, Or, Implies, Not, Equivalent, Symbol
from sympy.logic.boolalg import to_cnf

class Clause:
    def __init__(self, expression):
        self.expression = expression.strip()
        self.symbols = {}  # Store symbols as a dictionary for easy access
        self.postfix = self.infix_to_postfix(self.expression)
        self.count = 0

    def set_propositional_symbol(self, model):
        for symbol_name, symbol_obj in self.symbols.items():
            if symbol_name in model:
                symbol_obj.set_propositional_symbol(model)

    def get_count(self):
        if len(self.postfix) >= 3:
            self.count = len(self.symbols) - 1
        return self.count

    def isInferredSymbol(self):
        return len(self.postfix) == 1

    def __str__(self):
        return f"{self.expression}, postfix: {self.postfix}"

    def get_symbols(self):
        return list(self.symbols.keys())

    def get_value(self, symbol):
        symbol_obj = self.symbols.get(symbol)
        return symbol_obj.get_value() if symbol_obj else None

    def evaluate(self):
        stack = []
        for token in self.postfix:
            if isinstance(token, PropositionalSymbol):
                stack.append(token.get_value())
            elif token == '~':
                operand = stack.pop()
                stack.append(not operand)
            else:
                right = stack.pop()
                if token in ['&', '||', '=>', '<=>'] and stack:
                    left = stack.pop()
                if token == '&':
                    stack.append(left and right)
                elif token == '||':
                    stack.append(left or right)
                elif token == '=>':
                    stack.append(not left or right)
                elif token == '<=>':
                    stack.append(left == right)
        return stack.pop() if stack else None

    def infix_to_postfix(self, expression):
        precedence = {'~': 3, '&': 2, '||': 1, '=>': 0, '<=>': 0}
        stack = []
        postfix = []
        tokens = re.findall(r"\s*([a-zA-Z][a-zA-Z0-9]*|<=>|=>|&|\|\||~|\(|\))\s*", expression)

        for token in tokens:
            token = token.strip()
            if re.match(r"[a-zA-Z][a-zA-Z0-9]*", token):
                if token not in self.symbols:
                    self.symbols[token] = PropositionalSymbol(token)
                postfix.append(self.symbols[token])
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    postfix.append(stack.pop())
                stack.pop()
            else:
                while stack and stack[-1] != '(' and precedence[token] <= precedence.get(stack[-1], -1):
                    postfix.append(stack.pop())
                stack.append(token)

        while stack:
            postfix.append(stack.pop())

        return postfix

    def to_cnf(self):
        stack = []
        symbol_to_int = {symbol: idx + 1 for idx, symbol in enumerate(self.symbols)}

        for token in self.postfix:
            if isinstance(token, PropositionalSymbol):
                stack.append(sympy.Symbol(token.symbol))
            elif token == '~':
                operand = stack.pop()
                stack.append(sympy.Not(operand))
            else:
                right = stack.pop()
                if stack:
                    left = stack.pop()
                if token == '&':
                    stack.append(sympy.And(left, right))
                elif token == '||':
                    stack.append(sympy.Or(left, right))
                elif token == '=>':
                    stack.append(sympy.Implies(left, right))
                elif token == '<=>':
                    stack.append(sympy.Equivalent(left, right))

        expression = stack.pop() if stack else None
        cnf_expression = to_cnf(expression, simplify=True)

        clauses = str(cnf_expression).split(" & ")
        cnf_clauses = []

        for clause in clauses:
            literals = re.findall(r'[a-zA-Z][a-zA-Z0-9]*', clause)
            cnf_clause = []
            for literal in literals:
                negated = False
                if "~" + literal in clause:
                    negated = True
                symbol_index = symbol_to_int[literal]
                cnf_clause.append(-symbol_index if negated else symbol_index)
            cnf_clauses.append(cnf_clause)

        return cnf_clauses
