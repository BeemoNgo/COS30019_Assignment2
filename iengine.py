import sys
from parse import Parse
from clause import Clause
from propositionalSymbol import PropositionalSymbol
from TT import TT
from FC import FC
from BC import BC
# from WSAT import WSAT
from DPLL import DPLL
parse = Parse()
parse.readfile("test_HornKB.txt")
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
tt = TT()
tt.infer(parse.knowledge_base, parse.query)
print(tt.output)

print("DPLL method")
dpll = DPLL()  # Create an instance of DPLL
result = dpll.infer(parse.knowledge_base, parse.symbols)  # Infer using the knowledge base and symbols
print(result)  # Print the result returned by the DPLL algorithm



# method = {"tt":TT,"fc": FC,"bc":BC, "wsat":WSAT}
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