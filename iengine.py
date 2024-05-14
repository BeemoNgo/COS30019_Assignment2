import sys
import unittest
from parse import Parse
from clause import Clause
from propositionalSymbol import PropositionalSymbol
from TT import TruthTable
from FC import FC
from BC import BC
parse = Parse()
parse.readfile("test_HornKB.txt")
# print(parse.symbols)
# print(parse.knowledge_base)
fc = FC()
fc.infer(parse.knowledge_base, parse.query)
print(fc.output)

bc = BC()
bc.infer(parse.knowledge_base, parse.query)
print(bc.output)
# tt = TruthTable()
# tt.infer(parse.knowledge_base, parse.query)
# print(tt.output)
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