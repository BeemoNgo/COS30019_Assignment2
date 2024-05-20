from propositionalSymbol import PropositionalSymbol
import re
import sympy
from sympy import And, Or, Implies, Not, Equivalent, Symbol

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

    def isInferredSymbol(self): #checks if the clause represents an inferred symbol
        if len(self.postfix) == 1:
            return True
        return False

    def __str__(self) -> str:
        return f"{self.expression}, postfix:{self.postfix}"

    def get_symbols(self): #a list of symbols present in the clause
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
            if isinstance(token, PropositionalSymbol):  #check if token is a PropositionalSymbol
                stack.append(token.get_value())
            elif token == '~': #if token is negation
                operand = stack.pop()
                stack.append(not operand) #apply negation and push the result to the stack
            else:
                right = stack.pop() # Pop the right operand from the stack
                if token in ['&', '||', '=>', '<=>'] and stack: #check if stack is not empty for binary operators
                    left = stack.pop() #pop the left operand from the stack
                if token == '&': # Logical AND
                    stack.append(left and right) #perform AND operation and push result to stack
                elif token == '||': # Logical OR
                    stack.append(left or right) #perform OR operation and push result to stack
                elif token == '=>': # Implication
                    stack.append(not left or right) # Perform implication operation and push result to stack
                elif token == '<=>': # Equivalence
                    stack.append(left == right) # Perform equivalence operation and push result to stack
        return stack.pop() if stack else None



    def infix_to_postfix(self, expression):
        """
        Convert infix expression to postfix expression using the Shunting Yard algorithm.
        """
        precedence = {'~': 3, '&': 2, '||': 1, '=>': 0, '<=>': 0} # Define operator precedence

        stack = [] # store operators and parentheses
        postfix = [] #store the resulting postfix expression
        # Tokenize the input expression
        tokens = re.findall(r"\s*([a-zA-Z][a-zA-Z0-9]*|<=>|=>|&|\|\||~|\(|\))\s*", expression)

        for token in tokens:
            token = token.strip() # Remove leading and trailing spaces
            if re.match(r"[a-zA-Z][a-zA-Z0-9]*", token): # If token is a symbol
                if token not in self.symbols:
                    self.symbols[token] = PropositionalSymbol(token) #If the symbol is not in self.symbols,
                                                        #it creates a new PropositionalSymbol object and adds it to self.symbols.
                postfix.append(self.symbols[token])
            elif token == '(': # If token is an opening parenthesis
                stack.append(token)
            elif token == ')': # If token is a closing parenthesis
                while stack and stack[-1] != '(': # Pop operators from the stack until matching '(' is found
                    postfix.append(stack.pop())
                stack.pop() # Pop the '(' from stack
            else: # If token is an operator
                while (stack and stack[-1] != '(' and
                       precedence[token] <= precedence.get(stack[-1], -1)): # Operator precedence handling
                    postfix.append(stack.pop()) # Pop higher precedence operators and append to postfix
                stack.append(token) # Push current operator to stack

        while stack: # Pop remaining operators from stack and append to postfix
            postfix.append(stack.pop())

        return postfix
    
    def to_cnf(self):
        symbols = list(self.symbols.keys()) # Get a list of symbol names
        cnf_clauses = []
        postfix = self.postfix # Get the postfix expression
        stack = []

        for token in postfix: # Iterate through tokens in postfix expression
            if isinstance(token, PropositionalSymbol):
                stack.append(token.symbol) # Push symbol name to stack
            elif token == '~': # If token is negation
                operand = stack.pop()
                stack.append(f"~{operand}") # Add negation to operand and push to stack
            else:
                right = stack.pop()
                left = stack.pop()
                if token == '&': # Logical AND
                    stack.append(f"({left} & {right})") # Create CNF clause for AND operation
                elif token == '||': # Logical OR
                    stack.append(f"({left} || {right})")
                elif token == '=>': # Implication
                    stack.append(f"(~{left} || {right})")
                elif token == '<=>': # Equivalence
                    stack.append(f"(({left} & {right}) || (~{left} & ~{right}))")

        expression = stack.pop() # Get the final CNF expression
        expression = expression.replace("&", " and ").replace("||", " or ").replace("~", "not ") # Format expression
        cnf_expression = sympy.to_cnf(expression) # Convert expression to CNF using sympy
        cnf_clauses_str = str(cnf_expression).replace("(", "").replace(")", "").split(" & ") # Split CNF expression into clauses

        for clause_str in cnf_clauses_str:  # Iterate through CNF clauses
            clause = clause_str.replace(" or ", "").split("|")  # Split clause into literals
            cnf_clause = []  # Initialize list for CNF clause
            for literal in clause: 
                literal = literal.strip()  # Remove leading and trailing spaces
                if literal.startswith("not"):  # If literal is negated
                    symbol_name = literal[4:]  # Get symbol name
                    if symbol_name in symbols:  # Check if symbol exists
                        cnf_clause.append(-(symbols.index(symbol_name) + 1))  # Add negated symbol index to clause
                else:  # If literal is not negated
                    if literal in symbols:  # Check if symbol exists
                        cnf_clause.append(symbols.index(literal) + 1)  # Add symbol index to clause
            cnf_clauses.append(cnf_clause)  # Append CNF clause to list of CNF clauses

        return cnf_clauses  # Return CNF clauses
