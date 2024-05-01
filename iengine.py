import sys
import unittest
from parse import Parse
from clause import Clause
from propositionalSymbol import PropositionalSymbol
parse = Parse()
parse.readfile("test_genericKB_1.txt")
print(parse.knowledge_base)
# print(parse.query)
# a= PropositionalSymbol("a", True)
# print(a, a.get_value())
# a.set_propositional_symbol({"a":False,"b":True})
# print(a, a.get_value())
# test= Clause("a & b")
# test.set_propositional_symbol({"a":True,"b":False})
# print(test.evaluate())
