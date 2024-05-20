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
        temp = [x for x in query.symbols.keys()]  # Get list of symbols from the query
        lst = []
        for x in kb:  
            t1 = x.get_symbols()  # Get symbols from each clause
            lst.extend(t1)  # Extend list with symbols
        temp.extend(lst) 
        temp = list(set(temp))  # Remove duplicates and convert to list
        symbols = {} 
        for x in temp:  # Iterate through unique symbols
            symbols[x] = PropositionalSymbol(x, False) 

        self.TTCheckAll(kb, query, list(symbols.keys()), {})  # Perform truth table enumeration
        if self.check == "NO":  # If check is "NO" (unsatisfiable)
            self.output = "NO" 
        else:
            self.output = f"YES: {self.count}"  
    
    def PLTrue(self, kb, model):
        for x in kb: 
            x.set_propositional_symbol(model)  # Set symbols in the clause using the model
            if x.evaluate() == False:  # If clause is not true in the model
                return False 
        return True  

    def TTCheckAll(self, kb, query, symbols, model):
        if self.check == "NO":  # If already unsatisfiable
            return  # Exit recursion

        if len(symbols) == 0:  # If no symbols left to assign
            if self.PLTrue(kb, model):  # If the model satisfies the knowledge base
                query.set_propositional_symbol(model)  # Set symbols in query using the model
                if query.evaluate():  # If the model satisfies the query
                    self.count += 1  # Increment count of true assignments
                else:
                    self.check = "NO" 
        else:
            first_symbol = symbols.pop(0)  # Get and remove first symbol from symbols list

            new_model_true = copy.deepcopy(model)  # Create a deep copy of the model
            new_model_false = copy.deepcopy(model)  # Create another deep copy of the model

            new_model_true[first_symbol] = True  # Assign the first symbol as True in one copy
            self.TTCheckAll(kb, query, copy.deepcopy(symbols), new_model_true)  # Recurse with true assignment

            new_model_false[first_symbol] = False  # Assign the first symbol as False in the other copy
            self.TTCheckAll(kb, query, copy.deepcopy(symbols), new_model_false)  # Recurse with false assignment
