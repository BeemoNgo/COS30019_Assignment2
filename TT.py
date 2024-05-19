import sys
sys.setrecursionlimit(10000)
import copy
from propositionalSymbol import PropositionalSymbol

class TT:
    def __init__(self):
        self.output = ""
        self.count = 0
        self.check = None

    def getOutput(self):
        return self.output

    def infer(self, kb, query):
        # Collect all unique symbols from both the query and the knowledge base
        
        temp = [ x for x in query.symbols.keys()]  # Assuming query.symbols returns a list of PropositionalSymbol instances
        lst = []
        for x in kb:
            t1 = x.get_symbols()
            lst.extend(t1)
        temp.extend(lst)
        temp = list(set(temp))
        symbols = {}
        for x in temp:
            symbols[x] = PropositionalSymbol(x,False)
        
        self.TTCheckAll(kb, query, list(symbols.keys()), {})
        if self.check == "NO":
            self.output = "NO"
        else:
            self.output = f"YES: {self.count}"
    
    def PLTrue(self,kb, model):
        for x in kb:
            x.set_propositional_symbol(model)
            if x.evaluate() == False:
                return False
        return True

    def TTCheckAll(self, kb, query, symbols, model):
        if self.check == "NO":
            return

        if len(symbols) == 0:
            if self.PLTrue(kb,model):  # If the model satisfies the knowledge base
                query.set_propositional_symbol(model)
                if query.evaluate():  # If the model satisfies the query
                    self.count += 1
                else:
                    self.check = "NO"
        else:
            first_symbol = symbols.pop(0)

            new_model_true = copy.deepcopy(model)
            new_model_false = copy.deepcopy(model)

            new_model_true[first_symbol] = True
            self.TTCheckAll(kb, query, copy.deepcopy(symbols), new_model_true)  # Recurse with true assignment

            new_model_false[first_symbol] = False
            self.TTCheckAll(kb, query, copy.deepcopy(symbols), new_model_false)  # Recurse with false assignment
