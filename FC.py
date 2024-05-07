

class ForwardChaining:
    def __init__(self, knowledge_base, query, true_values, facts, agenda):
        self.knowledge_base = knowledge_base
        self.query = query
        self.true_values = true_values
        self.facts = facts
        self.agenda = agenda

    def forward_chain(self):
        result = False

        # Check if query is already true
        if self.query in self.facts:
            return True

        # Loop until a solution is found
        while self.agenda:
            new_added = False

            # For every rule in the agenda, check if it can be proven
            for antecedent, consequent in self.agenda:
                valid_rule = True

                # Check if all variables in the antecedent are true
                for dep_var in antecedent:
                    if dep_var not in self.facts:
                        valid_rule = False
                        break

                if valid_rule:
                    # Add consequent to the list of known facts
                    if consequent not in self.facts:
                        new_added = True
                        self.facts.add(consequent)
                        self.true_values.put(consequent)

                    # Check if consequent is the same as the query
                    if consequent == self.query:
                        result = True
                        break

            # If no new facts were added in the last iteration, stop
            if not new_added:
                break

        return result
    