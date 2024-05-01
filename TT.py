import sys
sys.setrecursionlimit(10000)

class TruthTable:
    def __init__(self):
        self.output = ""
        self.count = 0
        self.check = None

    def getOutput(self):
        return self.output

    def infer(self, kb, query):
        # Collect all unique symbols from both the query and the knowledge base
        temp = [x.symbol for x in query.symbols]  # Assuming query.symbols returns a list of PropositionalSymbol instances
        list = {x.symbol: False for x in kb.symbols}  # Assuming kb.symbols is also a list of PropositionalSymbol instances
        for x in temp:
            list[x] = False  # Ensuring all symbols are unique and initialized to False

        symbols = list(list.keys())
        self.TTCheckAll(kb, query, symbols, {})
        if self.check == "NO":
            self.output = "NO"
        else:
            self.output = f"YES: {self.count}"

    def TTCheckAll(self, kb, query, symbols, model):
        if self.check == "NO":
            return

        if len(symbols) == 0:
            if kb.PLTrue(model):  # If the model satisfies the knowledge base
                query.setValues(model)
                if query.evaluate():  # If the model satisfies the query
                    self.count += 1
                else:
                    self.check = "NO"
        else:
            first_symbol = symbols.pop(0)
            new_model_true = model.copy()
            new_model_false = model.copy()
            new_model_true[first_symbol] = True
            new_model_false[first_symbol] = False

            self.TTCheckAll(kb, query, symbols.copy(), new_model_true)  # Recurse with true assignment
            self.TTCheckAll(kb, query, symbols.copy(), new_model_false)  # Recurse with false assignment
