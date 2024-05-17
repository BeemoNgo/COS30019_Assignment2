from propositionalSymbol import PropositionalSymbol
import re
# from sympy import And, Or, Implies, Not, Equivalent, Symbol
# from sympy.parsing.sympy_parser import parse_expr

class Clause:
    def __init__(self, expression):
        self.expression = expression.strip()
        self.symbols = {}  # Store symbols as a dictionary for easy access
        self.postfix = self.infix_to_postfix(self.expression)
        self.count = 0

    def set_propositional_symbol(self, model):
        """
        Set the values of the propositional symbols based on the provided model.
        """
        for symbol_name, symbol_obj in self.symbols.items():
            if symbol_name in model:
                symbol_obj.set_propositional_symbol(model)

    def get_count(self):
        if len(self.postfix) >=3:
            self.count = len(self.symbols)-1
        return self.count

    def isInferredSymbol(self):
        if len(self.postfix) == 1:
            return True
        return False

    def __str__(self) -> str:
        return f"{self.expression}, postfix:{self.postfix}"

    def get_symbols(self):
        temp = []
        for x in self.symbols:
            temp.append(x)
        return temp

    def get_value(self, symbol):
        """
        Retrieve the value of a specific propositional symbol if it has been set.
        """
        symbol_obj = self.symbols.get(symbol)
        return symbol_obj.get_value() if symbol_obj else None

    def evaluate(self):
        """
        Evaluate the logical expression based on the current values of the propositional symbols.
        """
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
        """
        Convert infix expression to postfix expression using the Shunting Yard algorithm.
        """
        precedence = {'~': 3, '&': 2, '||': 1, '=>': 0, '<=>': 0}
        stack = [] # store operators and parentheses
        postfix = [] #store the resulting postfix expression
        # Improved tokenization to handle symbols with numbers and operators, considering spaces
        tokens = re.findall(r"\s*([a-zA-Z][a-zA-Z0-9]*|<=>|=>|&|\|\||~|\(|\))\s*", expression)

        for token in tokens:
            token = token.strip()
            if re.match(r"[a-zA-Z][a-zA-Z0-9]*", token):
                if token not in self.symbols:
                    self.symbols[token] = PropositionalSymbol(token) #If the symbol is not in self.symbols,
                                                        #it creates a new PropositionalSymbol object and adds it to self.symbols.
                postfix.append(self.symbols[token])
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    postfix.append(stack.pop())
                stack.pop()
            else:
                while (stack and stack[-1] != '(' and
                       precedence[token] <= precedence.get(stack[-1], -1)):
                    postfix.append(stack.pop())
                stack.append(token)

        while stack:
            postfix.append(stack.pop())

        return postfix