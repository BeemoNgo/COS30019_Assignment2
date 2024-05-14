import sys
sys.setrecursionlimit(10000)
from clause import Clause

class BC:
    def __init__(self):
        self.output = ""

    def getOutput(self):
        return self.output

    def infer(self, kb, query):
        propositionalSymbolList = {symbol: None for clause in kb for symbol in clause.get_symbols()}
        provenSymbol = []  # List to keep track of the order of proven symbols

        for clause in kb:
            if clause.isInferredSymbol():  # If the clause is a known fact
                propositionalSymbolList[clause.get_symbols()[0]] = True
                provenSymbol.append(clause.get_symbols()[0])

        result = self.bc_recursive(kb, query, propositionalSymbolList, provenSymbol)
        if result:
            self.output = "YES: " + ', '.join(provenSymbol)
            print(provenSymbol)
        else:
            self.output = "NO"
        return result

    def bc_recursive(self, kb, query, propositionalSymbolList, provenSymbol):
        if query.get_symbols()[0] in propositionalSymbolList:
            if propositionalSymbolList[query.get_symbols()[0]] is True:
                return True
            elif propositionalSymbolList[query.get_symbols()[0]] is False:
                return False

        # Check if any clause in KB concludes the query symbol
        for clause in kb:
            if clause.get_symbols()[-1] == query.get_symbols()[0]:  # Check if clause conclusion matches query
                all_antecedents_met = True
                temp_proven = []  # Temporary list for this path of reasoning
                for antecedent in clause.get_symbols()[:-1]:  # Check each antecedent in the clause
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
