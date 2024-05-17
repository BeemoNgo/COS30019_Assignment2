from clause import *

"""
This class implements a simple backward chaining algorithm for propositional logic.

- The `BC` class is initialized with an empty `output`.
- The `infer` method takes a knowledge base `kb` and a `query`.
- The `propositionalSymbolList` dictionary is initialized to track which symbols have been inferred as true or false.
- The `provenSymbol` list keeps track of the order in which symbols have been proven true.

The algorithm:
1. Initializes `propositionalSymbolList` and `provenSymbol`.
2. Calls the recursive method `bc_recursive` to determine if the query can be inferred from the knowledge base.
3. Updates `output` based on whether the query is inferred.

The `bc_recursive` method:
1. Checks if the query symbol is already known and returns its truth value.
2. Iterates through the clauses in the knowledge base to find those that conclude the query symbol.
3. Recursively checks each antecedent of these clauses.
4. If all antecedents are proven true, the query symbol is set to true, and the proven symbols are updated.
5. If no clause supports the query symbol, it is set to false.

"""

class BC:
    def __init__(self):
        self.output = ""

    def infer(self, kb, query):
        propositionalSymbolList = {}
        provenSymbol = []  # List to keep track of the order of proven symbols

        result = self.bc_recursive(kb, query, propositionalSymbolList, provenSymbol)
        if result:
            self.output = "YES: " + ', '.join(provenSymbol)
        else:
            self.output = "NO"
        return result

    def bc_recursive(self, kb, query, propositionalSymbolList, provenSymbol):
        # Check if the query symbol is already known
        if query.get_symbols()[0] in propositionalSymbolList:
            return propositionalSymbolList[query.get_symbols()[0]]

        # Check if any clause in KB concludes the query symbol
        for clause in kb:
            if clause.get_symbols()[-1] == query.get_symbols()[0]:  # Check if clause conclusion matches query
                all_antecedents_met = True
                temp_proven = []  # Temporary list for this path of reasoning

                # Check each antecedent in the clause
                for antecedent in clause.get_symbols()[:-1]:
                    if not self.bc_recursive(kb, Clause(antecedent), propositionalSymbolList, temp_proven):
                        all_antecedents_met = False
                        break

                if all_antecedents_met:
                    # If all antecedents are true, then the conclusion is true
                    propositionalSymbolList[query.get_symbols()[0]] = True
                    provenSymbol.extend(temp_proven)
                    provenSymbol.append(query.get_symbols()[0])  # Append the proven conclusion
                    return True

        propositionalSymbolList[query.get_symbols()[0]] = False
        return False
