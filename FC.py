from clause import *

"""
This class implements a simple forward chaining algorithm for propositional logic.

- The `FC` class is initialized with an empty `output`.
- The `infer` method takes a knowledge base `kb` and a `query`.
- The `propositionalSymbolList` dictionary is initialized to track which symbols have been inferred as true.
- The `agenda` list contains symbols that are known to be true initially.
- The `clauseCount` dictionary tracks how many premises of each clause are not yet proven.

The algorithm:
1. Initializes `propositionalSymbolList` and `agenda` with symbols from `kb`.
2. Sets up `clauseCount` to track how many premises are left to prove for each clause.
3. Checks if the `query` is already in the `agenda`.
4. Processes the `agenda` by iterating through symbols, 
   updating the `propositionalSymbolList`, and decrementing `clauseCount` when symbols are found in clauses.
5. If the `query` is found during processing, it updates `output` to indicate success; otherwise, it indicates failure.

"""

class FC:
    def __init__(self) -> None:
        self.output = ""

    def infer(self, kb, query):
        propositionalSymbolList = {}
        agenda = []
        clauseCount = {}  # Dictionary to keep count of how many premises of each clause are not yet proven

        # Initialize the propositionalSymbolList and agenda
        for clause in kb:
            for symbol in clause.get_symbols():
                propositionalSymbolList[symbol] = False
                if clause.isInferredSymbol():
                    agenda.append(symbol)

        # Initialize the count for each clause
        for clause in kb:
            clauseCount[clause] = clause.get_count()

        # Check if the query is already a known fact
        if query.isInferredSymbol() and query.get_symbols()[0] in agenda:
            self.output = "YES: " + query.get_symbols()[0]
            return query.get_symbols()
        
        # Process the agenda
        while len(agenda) > 0:
            currentSymbol = agenda.pop(0)  # Get the next symbol in the list of true symbols
            if currentSymbol == query.get_symbols()[0]:
                self.output = "YES: " + self.output + currentSymbol
                return
            if not propositionalSymbolList[currentSymbol]:
                propositionalSymbolList[currentSymbol] = True
                self.output += currentSymbol + ", "
                for clause in kb:
                    for i in range(len(clause.get_symbols()) - 1):
                        if clause.get_symbols()[i] == currentSymbol:
                            if clauseCount[clause] > 0:
                                clauseCount[clause] -= 1
                                if clauseCount[clause] <= 0:
                                    if clause.get_symbols()[-1] == query.get_symbols()[0]:
                                        self.output = "YES: " + self.output + clause.get_symbols()[-1]
                                        return
                                    agenda.append(clause.get_symbols()[-1])

        self.output = "NO"


