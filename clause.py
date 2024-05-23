from propositionalSymbol import PropositionalSymbol
import re
import sympy
from sympy.logic.boolalg import to_cnf

class Clause:
    def __init__(self, expression):
        self.expression = expression.strip()
        self.symbols = {}
        self.postfix = self.infix_to_postfix(self.expression)

    def set_propositional_symbol(self, model):  # Method to set propositional symbols based on a model
        for symbol_name, symbol_obj in self.symbols.items():
            if symbol_name in model:  # Checking if the symbol exists in the model
                symbol_obj.set_propositional_symbol(model)  # Setting the propositional symbol using the model

    def isInferredSymbol(self):  # Method to check if the clause represents an inferred symbol
        return len(self.postfix) == 1  # Returning True if the postfix notation has only one element (inferred symbol)

    def __str__(self):  # Method to return a string representation of the Clause object
        return f"{self.expression}, postfix: {self.postfix}"

    def get_symbols(self):  # Method to get a list of symbols used in the clause
        return list(self.symbols.keys())  # Returning the list of symbols

    def get_value(self, symbol):  # Method to get the truth value of a symbol in the clause
        symbol_obj = self.symbols.get(symbol)  # Getting the symbol object from the symbols dictionary
        return symbol_obj.get_value() if symbol_obj else None  # Returning the symbol's value if it exists, else None

    def evaluate(self):  # Method to evaluate the truth value of the clause
        stack = []
        for token in self.postfix:  # Looping through tokens in the postfix notation
            if isinstance(token, PropositionalSymbol):  # Checking if the token is a PropositionalSymbol object
                stack.append(token.get_value())  # Appending the symbol's value to the stack
            elif token == '~':  # Handling negation operator
                operand = stack.pop()  # Popping the operand from the stack
                stack.append(not operand)  # Appending the negation of the operand to the stack
            else:  # Handling logical operators
                right = stack.pop()  # Popping the right operand from the stack
                if token in ['&', '||', '=>', '<=>'] and stack:  # Checking if operator requires a left operand
                    left = stack.pop()  # Popping the left operand from the stack
                if token == '&':  # Handling conjunction
                    stack.append(left and right)  # Appending the result of AND operation to the stack
                elif token == '||':  # Handling disjunction
                    stack.append(left or right)  # Appending the result of OR operation to the stack
                elif token == '=>':  # Handling implication
                    stack.append(not left or right)  # Appending the result of implication to the stack
                elif token == '<=>':  # Handling biconditional
                    stack.append(left == right)  # Appending the result of equivalence to the stack
        return stack.pop() if stack else None

    def infix_to_postfix(self, expression):  # Method to convert an infix expression to postfix notation
        precedence = {'~': 3, '&': 2, '||': 1, '=>': 0, '<=>': 0}  # Operator precedence dictionary
        stack = []
        postfix = []  # Initializing an empty list for postfix notation
        tokens = re.findall(r"\s*([a-zA-Z][a-zA-Z0-9]*|<=>|=>|&|\|\||~|\(|\))\s*", expression)  # Tokenizing the expression

        for token in tokens:
            token = token.strip()  # Stripping whitespace from the token
            if re.match(r"[a-zA-Z][a-zA-Z0-9]*", token):  # Checking if the token is a symbol
                if token not in self.symbols:  # Checking if the symbol is not already in the symbols dictionary
                    self.symbols[token] = PropositionalSymbol(token)  # Creating a new PropositionalSymbol object
                postfix.append(self.symbols[token])  # Appending the symbol to the postfix notation
            elif token == '(':  # Handling left parenthesis
                stack.append(token)  # Pushing the left parenthesis onto the stack
            elif token == ')':  # Handling right parenthesis
                while stack and stack[-1] != '(':  # Popping operators until left parenthesis is encountered
                    postfix.append(stack.pop())  # Appending popped operators to postfix notation
                stack.pop()  # Removing the left parenthesis from the stack
            else:  # Handling operators
                while stack and stack[-1] != '(' and precedence[token] <= precedence.get(stack[-1], -1):
                    postfix.append(stack.pop())  # Appending popped operators to postfix notation
                stack.append(token)  # Pushing the current operator onto the stack

        while stack:  # Popping remaining operators from the stack
            postfix.append(stack.pop())  # Appending popped operators to postfix notation

        return postfix  # Returning the postfix notation

    def to_cnf(self):  # Method to convert the clause to Conjunctive Normal Form (CNF)
        stack = []
        for token in self.postfix:
            if isinstance(token, PropositionalSymbol):  # Checking if the token is a PropositionalSymbol object
                stack.append(sympy.Symbol(token.symbol))  # Appending the symbol as a sympy Symbol object
            elif token == '~':  # Handling negation operator
                operand = stack.pop()  # Popping the operand from the stack
                stack.append(sympy.Not(operand))  # Appending the negation of the operand to the stack
            else:  # Handling logical operators
                right = stack.pop()  # Popping the right operand from the stack
                if token in ['&', '||', '=>', '<=>'] and stack:  # Checking if operator requires a left operand
                    left = stack.pop()  # Popping the left operand from the stack
                if token == '&':  # Handling conjunction
                    stack.append(sympy.And(left, right))  # Appending the result of AND operation to the stack
                elif token == '||':  # Handling disjunction
                    stack.append(sympy.Or(left, right))  # Appending the result of OR operation to the stack
                elif token == '=>':  # Handling implication
                    stack.append(sympy.Implies(left, right))  # Appending the result of implication to the stack
                elif token == '<=>':  # Handling biconditional
                    stack.append(sympy.Equivalent(left, right))  # Appending the result of equivalence to the stack

        expression = stack.pop() if stack else None  # Getting the final expression from the stack
        cnf_expression = to_cnf(expression, simplify=True)  # Converting the expression to CNF

        clauses = str(cnf_expression).split(" & ")  # Splitting CNF expression into individual clauses
        cnf_clauses = []  # Initializing a list to store CNF clauses

        for clause in clauses:  # Looping through clauses
            literals = re.findall(r'(~?[a-zA-Z][a-zA-Z0-9]*)', clause)  # Extracting literals from each clause
            cnf_clause = []  # Initializing a list for the CNF clause
            for literal in literals:  # Looping through literals
                cnf_clause.append(literal)  # Appending literals to CNF clause
            cnf_clauses.append(cnf_clause)  # Appending CNF clause to list of CNF clauses

        return cnf_clauses  # Returning the CNF clauses
