class RES:
    def __init__(self):
        self.output = ""

    def getOutput(self):
        return self.output

    def infer(self, kb, query):
        cnf_formula = []
        for clause in kb:
            cnf_formula.extend(clause.to_cnf())
        query_clause = query.to_cnf()
        cnf_formula.extend(query_clause)

        # Convert list of lists to set of frozensets for resolution
        clauses = set(frozenset(clause) for clause in cnf_formula)
        if self.resolution_algorithm(clauses):
            self.output = "NO"
        else:
            self.output = "YES"

        return self.output

    def resolve(self, c1, c2):
        """ Attempt to resolve two clauses c1 and c2, return None if no resolution is possible. """
        for lit in c1:
            if -lit in c2:
                # Create a new clause without the resolved literal
                new_clause = set(c1)
                new_clause.remove(lit)
                new_clause.update(c2)
                new_clause.remove(-lit)
                return frozenset(new_clause)
        return None

    def resolution_algorithm(self, clauses):
        """ Applies the resolution algorithm on a set of clauses, returns if it's unsatisfiable. """
        new = set()
        clauses_list = list(clauses)  # Convert set to list for indexing
        while True:
            n = len(clauses_list)
            pairs = [(clauses_list[i], clauses_list[j]) for i in range(n) for j in range(i + 1, n)]

            for (ci, cj) in pairs:
                resolvent = self.resolve(ci, cj)
                if resolvent is not None:
                    if len(resolvent) == 0:
                        return True  # Unsatisfiable (empty clause found)
                    new.add(resolvent)

            if new.issubset(clauses):  # No new clauses, satisfiable
                return False
            clauses.update(new)
            clauses_list = list(clauses)  # Update the list with new clauses

    