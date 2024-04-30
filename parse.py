import sympy 
from sympy import And, Or, Implies, Not, Equivalent, Symbol
from sympy.parsing.sympy_parser import parse_expr
import random
import string
import re
import unittest

class Parse():
    def __init__(self):
        self.knowledge_base = []
        self.query = None

    def readfile(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read()

        # Split the content based on the TELL and ASK keywords
        tell_section, ask_section = content.split('ASK')
        tell_content = tell_section.split('TELL')[1]

        # Remove unwanted whitespace and newlines
        tell_clauses = tell_content.strip().split(';')
        self.query = ask_section.strip()

        # Remove extra whitespace around clauses
        self.knowledge_base = [clause.strip() for clause in tell_clauses if clause.strip()]

        # This is where you would convert clauses into your specific Clause objects if necessary
        # For example: self.knowledge_base = [Clause(clause) for clause in self.knowledge_base]

        return self.knowledge_base, self.query