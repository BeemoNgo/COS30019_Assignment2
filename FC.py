class FC:  
    def __init__(self) -> None: 
        self.output = ""  

    def getOutput(self):  
        return self.output 

    def infer(self, kb, query): 
        propositionalSymbolList = {}  # Initialize a dictionary to track propositional symbols
        agenda = []  # Initialize a list for the agenda
        clauseCount = {}  # Initialize a dictionary to keep count of premises for each clause

        for clause in kb: 
            for symbol in clause.get_symbols():  # Loop through symbols in each clause
                propositionalSymbolList[symbol] = False  # Add symbols to propositional symbol list
                if clause.isInferredSymbol(): 
                    agenda.append(symbol)  

        for clause in kb:  
            clauseCount[clause] = clause.get_count()  # Initialize premise count for each clause

        if query.isInferredSymbol() and query.get_symbols()[0] in agenda:  # Check if query is already known
            self.output = "YES: " + query.get_symbols()[0]  # Set output as "YES" with query symbol
            return 

        while len(agenda) > 0:  # While agenda is not empty
            currentSymbol = agenda.pop(0)  # Get the next symbol from agenda
            if currentSymbol == query.get_symbols()[0]:  # If current symbol matches query
                self.output = "YES: " + self.output + currentSymbol  
                return  
            if propositionalSymbolList[currentSymbol] == False:  # If current symbol is not yet proven
                propositionalSymbolList[currentSymbol] = True  # Mark current symbol as true
                self.output += currentSymbol + ", "  # Append current symbol to output
                for clause in kb:  
                    for i in range(len(clause.get_symbols()) - 1):  # Loop through symbols in clauses
                        if clause.get_symbols()[i] == currentSymbol:  # If symbol matches current symbol
                            if clauseCount[clause] > 0:  # If premises of clause are not fully proven
                                clauseCount[clause] -= 1  # Decrease premise count
                                if clauseCount[clause] <= 0:  # If all premises are proven
                                    if clause.get_symbols()[len(clause.get_symbols()) - 1] == query.get_symbols()[0]:  # If conclusion matches query
                                        self.output = "YES: " + self.output + clause.get_symbols()[len(clause.get_symbols()) - 1]  # Set output as "YES" with conclusion
                                        return 
                                    agenda.append(clause.get_symbols()[len(clause.get_symbols()) - 1])  # Add conclusion to agenda

        self.output = "NO"  # Set output as "NO" if query cannot be inferred
