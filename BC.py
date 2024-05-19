import sys
sys.setrecursionlimit(10000)
from clause import Clause

class BC:
    def __init__(self) -> None:
        self.output = "NO"
        self.outputSymbols = []

    def getOutput(self): 
        return self.output

    def infer(self, kb, query):
        if self.BC_recursion(kb, query.get_symbols()[0], []):
            self.output = "YES: "
            for symbol in self.outputSymbols:
                if symbol != query.get_symbols()[0]:
                    self.output += symbol + ", "
            self.output += query.get_symbols()[0]

    def BC_recursion(self, kb, query, explored):
        for clause in kb:
            if clause.isInferredSymbol() and clause.get_symbols()[0] == query:
                if query not in self.outputSymbols:
                    self.outputSymbols.append(query)
                return True

        for clause in kb:
            if clause.get_symbols()[-1] == query:
                leftHandSymbols = clause.get_symbols()[:-1]
                trueSymbolCount = 0
                for symbol in leftHandSymbols:
                    if symbol == query:
                        break
                    if symbol in explored:
                        if not self.BC_recursion(kb, symbol, explored):
                            break
                    else:
                        explored.append(symbol)
                    if not self.BC_recursion(kb, symbol, explored.copy()):
                        break
                    trueSymbolCount += 1

                if trueSymbolCount == len(leftHandSymbols):
                    if query not in self.outputSymbols:
                        self.outputSymbols.append(query)
                    return True
        return False
