import sys
import unittest
from parse import Parse
from clause import Clause
from propositionalSymbol import PropositionalSymbol
from TT import TruthTable
parse = Parse()
parse.readfile("test_HornKB.txt")
tt = TruthTable()
tt.infer(parse.knowledge_base, parse.query)
print(tt.output)
# a= PropositionalSymbol("a", True)
# print(a, a.get_value())
# a.set_propositional_symbol({"a":False,"b":True})
# print(a, a.get_value())
# test= Clause("(a || b) & a")
# test.set_propositional_symbol({"a":True,"b":False})
# print(test.postfix)
# print(test.evaluate())
# truth_table = TruthTable()
# truth_table.infer()