import sys
from parse import Parse
from clause import Clause
from propositionalSymbol import PropositionalSymbol
from TT import TT
from FC import FC
from BC import BC
from DPLL import DPLL
from RES import RES

class Environment:
    def __init__(self):
        self.knowledge_base = None
        self.query = None
        self.symbols = None
    
    def readFile(self, filename):
        parse = Parse()
        parse.readfile(filename)
        self.knowledge_base = parse.knowledge_base
        self.query = parse.query
        self.symbols = parse.symbols

def main():
    if len(sys.argv) != 3:
        raise Exception("Wrong number of arguments")
    
    filename = sys.argv[1]
    method = sys.argv[2]

    environment = Environment()
    environment.readFile(filename)

    methods = {
        "TT": TT,
        "FC": FC,
        "BC": BC,
        "DPLL": DPLL,
        "RES": RES
    }
    
    if method not in methods:
        raise Exception("There is no such method, the available methods are TT, FC, BC, DPLL, and RES")
    
    algorithm_class = methods[method]
    algorithm = algorithm_class()
    algorithm.infer(environment.knowledge_base, environment.query)
    print(algorithm.output)

if __name__ == "__main__":
    main()
        
# print("FC method")
# fc = FC()
# fc.infer(parse.knowledge_base, parse.query)
# print(fc.output)

# print("BC method")
# bc = BC()
# bc.infer(parse.knowledge_base, parse.query)
# print(bc.output)

# print("TT method")
# tt = TT()
# tt.infer(parse.knowledge_base, parse.query)
# print(tt.output)

# print("DPLL method")
# dpll = DPLL()  # Create an instance of DPLL
# result = dpll.infer(parse.knowledge_base, parse.symbols)  # Infer using the knowledge base and symbols
# print(result)  # Print the result returned by the DPLL algorithm

# print("RES method")
# resolution = RES()  # Create an instance of Resolution
# result = resolution.infer(parse.knowledge_base, parse.query)  # Infer using the knowledge base and query
# print(result)
