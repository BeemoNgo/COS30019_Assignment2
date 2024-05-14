import sys

class FC:
    def __init__(self) -> None:
        self.output = ""

    def getOutput(self):
        return self.output

    def infer(self, kb, query):
        propositionalSymbolList = {}
        agenda = []
        clauseCount = {} #dictionary to keep count of how many premises of each clause are not yet proven

        for clause in kb:
            for symbol in clause.get_symbols():
                propositionalSymbolList[symbol] = False
                if clause.isInferredSymbol():
                    agenda.append(symbol)

        for clause in kb: # Initiallize the count for each clause 
            clauseCount[clause] = clause.get_count()

        if query.isInferredSymbol() and query.get_symbols()[0] in agenda: # Check if the query is already a known fact
            self.output = "YES: " + query.get_symbols()[0]
            return
        
        while len(agenda) > 0:
            currentSymbol = agenda.pop(0)  # Get the next symbol in the list of true symbols
            if currentSymbol == query.get_symbols()[0]:
                self.output = "YES: " + self.output + currentSymbol
                return
            if (propositionalSymbolList[currentSymbol] == False):
                propositionalSymbolList[currentSymbol] = True
                self.output += currentSymbol + ", "
                for clause in kb: # Loop through the sentence in KB to find the symbol
                    # Loop through each symbol on the left hand side to find the symbol
                    for i in range(len(clause.get_symbols())-1):
                        if clause.get_symbols()[i] == currentSymbol:
                            if (clauseCount[clause] > 0):
                                clauseCount[clause] -= 1 # decrease the point when a match is found
                                # append the symbol when the count reaches 0
                                if  clauseCount[clause]  <= 0:
                                    # Check if the conclusion of the sentence contain the query
                                    if clause.get_symbols()[len(clause.get_symbols()) - 1] == query.get_symbols()[0]:
                                        self.output = "YES: " + self.output + clause.get_symbols()[len(clause.get_symbols()) - 1]
                                        return
                                    agenda.append(clause.get_symbols()[len(clause.get_symbols()) - 1])

        self.output = "NO"
