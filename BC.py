import sys  
sys.setrecursionlimit(10000)  

class BC:  
    def __init__(self) -> None:  
        self.output = "NO"  
        self.outputSymbols = [] 

    def getOutput(self):  
        return self.output  

    def infer(self, kb, query): 
        if self.BC_recursion(kb, query.get_symbols()[0], []):  # Call the BC_recursion method
            self.output = "YES: "  
            for symbol in self.outputSymbols: 
                if symbol != query.get_symbols()[0]:  # Exclude the query symbol from output
                    self.output += symbol + ", "  # Append symbols to output string
            self.output += query.get_symbols()[0]  # Append the query symbol to output string

    def BC_recursion(self, kb, query, explored):  # Recursive method for backward chaining
        for clause in kb:  
            if clause.isInferredSymbol() and clause.get_symbols()[0] == query:  # Check if clause is an inferred symbol
                if query not in self.outputSymbols:  # Add query symbol to output symbols if not already present
                    self.outputSymbols.append(query)
                return True  # Return True if query is found in KB as an inferred symbol

        for clause in kb:
            if clause.get_symbols()[-1] == query:  # Check if query is the conclusion of the clause
                leftHandSymbols = clause.get_symbols()[:-1]  # Get symbols on the left-hand side of the clause
                trueSymbolCount = 0  # Initialize a counter for true symbols
                for symbol in leftHandSymbols:  
                    if symbol == query:  # Break the loop if query is encountered
                        break
                    if symbol in explored:  # Check if symbol has been explored
                        if not self.BC_recursion(kb, symbol, explored):  # Recursively explore symbol
                            break  # Break the loop if recursion returns False
                    else:  # If symbol is not explored
                        explored.append(symbol)  # Add symbol to explored list
                    if not self.BC_recursion(kb, symbol, explored.copy()):  # Recursively explore symbol (copying explored list)
                        break  # Break the loop if recursion returns False
                    trueSymbolCount += 1  # Increment true symbol count

                if trueSymbolCount == len(leftHandSymbols):  # Check if all left-hand symbols are true
                    if query not in self.outputSymbols:  # Add query symbol to output symbols if not already present
                        self.outputSymbols.append(query)
                    return True  # Return True if all left-hand symbols are true
        return False  # Return False if query cannot be inferred from KB
 