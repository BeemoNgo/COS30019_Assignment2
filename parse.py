import sympy 
import random
import string
import re
from clause import Clause

class Parse():
    def __init__(self):
        self.knowledge_base = []
        self.query = None
        self.symbols = []

    def readfile(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()

        # Split the content based on the TELL and ASK keywords
        tell_section, ask_section = content.split('ASK')
        tell_content = tell_section.split('TELL')[1]

        # Remove unwanted whitespace and newlines
        tell_clauses = tell_content.strip().split(';')
        a = ask_section.strip()
        self.query = Clause(a)

        # Remove extra whitespace around clauses
        temp  = [clause.strip() for clause in tell_clauses if clause.strip()]
        # print(temp)
        for x in temp:
            self.knowledge_base.append(Clause(x))
        self.extract_symbols()
        return self.knowledge_base, self.query, self.symbols
    
    def extract_symbols(self):
        # Initialize a set to keep symbols unique
        symbol_set = set()

        # Extract symbols from each clause in the knowledge base
        for clause in self.knowledge_base:
            symbol_set.update(clause.get_symbols())

        # Extract symbols from the query
        if self.query:
            symbol_set.update(self.query.get_symbols())
        # # print(symbol_set)
        # # Convert the set to a list and assign to the symbols attribute
        self.symbols = list(symbol_set)