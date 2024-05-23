import sys
from parse import Parse
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
    method = sys.argv[2].lower()

    environment = Environment()
    environment.readFile(filename)

    methods = {
        "tt": TT,
        "fc": FC,
        "bc": BC,
        "dpll": DPLL,
        "res": RES
    }

    if method not in methods:
        raise Exception("There is no such method, the available methods are TT, FC, BC, DPLL, and RES")

    algorithm_class = methods[method]
    algorithm = algorithm_class()
    algorithm.infer(environment.knowledge_base, environment.query)
    print(algorithm.output)

if __name__ == "__main__":
    main()

