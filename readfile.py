import sympy 
from sympy import And, Or, Implies, Not, Equivalent, Symbol
from sympy.parsing.sympy_parser import parse_expr
import random
import string
import re
import unittest

class readfile():
    def __init__(self):
        self.symbols = [] # the list of symbols in the knowledge base
        self.knowledgeBase = []
        self.query = None

    def readfile(self, filename):
        with open(filename, 'r') as file:
            line = file.readline().strip()
            if line != "TELL":
                raise Exception("No TELL")