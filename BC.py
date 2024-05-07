

class BackwardChaining:
    def __init__(self, knowledge_base, query, true_values, facts, agenda):
        self.knowledge_base = knowledge_base
        self.query = query
        self.facts = facts
        self.agenda = agenda
        self.path = true_values

    def _backward_chain(self, query):
        # Check if query is a known fact
        if query in self.facts:
            return True

        # Check if query can be deduced from rules
        for antecedent, consequent in self.agenda:
            if query == consequent:
                # Check if all antecedents are true
                antecedents_true = all(self._backward_chain(var) for var in antecedent)
                if antecedents_true:
                    return True
        return False

    def backward_chain(self):
        return self._backward_chain(self.query)

