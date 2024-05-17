import sys
import unittest
from parse import Parse
from clause import Clause
from propositionalSymbol import PropositionalSymbol
from TT import TruthTable
from FC import FC
from BC import BC
parse = Parse()
parse.readfile("test.txt")
# print(parse.symbols)
# print(parse.knowledge_base)

print("FC method")
fc = FC()
fc.infer(parse.knowledge_base, parse.query)
print(fc.output)

print("BC method")
bc = BC()
bc.infer(parse.knowledge_base, parse.query)
print(bc.output)

print("TT method")
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