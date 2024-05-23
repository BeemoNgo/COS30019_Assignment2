from clause import Clause

class RES:
    def __init__(self):
        self.output = ""

    def getOutput(self):
        return self.output

    def infer(self, kb, query):
        cnf_formula = []
        for clause in kb:
            cnf_formula.extend(clause.to_cnf())  # Convert each clause to CNF and add to cnf_formula

        # Negate the query and convert it to CNF
        negated_query = Clause(f"~({query.expression})")
        query_clause = negated_query.to_cnf()
        cnf_formula.extend(query_clause)  # Add query CNF clause to cnf_formula

        # Convert CNF clauses to frozensets for resolution
        clauses = set(frozenset(clause) for clause in cnf_formula)
        if self.resolution_algorithm(clauses):
            self.output = "YES"  # Set output as "YES" if resolution algorithm finds unsatisfiable (entails the query)
        else:
            self.output = "NO"  # Set output as "NO" if resolution algorithm finds satisfiable (does not entail the query)
        return self.output

    def resolve(self, c1, c2):
        """ Attempt to resolve two clauses c1 and c2, return None if no resolution is possible. """
        for lit in c1:
            if self.negate_literal(lit) in c2:
                new_clause = set(c1)
                new_clause.remove(lit)
                new_clause.update(c2)
                new_clause.remove(self.negate_literal(lit))
                return frozenset(new_clause)
        return None

    def resolution_algorithm(self, clauses):
        """ Applies the resolution algorithm on a set of clauses, returns if it's unsatisfiable. """
        new = set()
        clauses_list = list(clauses)
        while True:
            n = len(clauses_list)
            pairs = [(clauses_list[i], clauses_list[j]) for i in range(n) for j in range(i + 1, n)]

            for (ci, cj) in pairs:
                resolvent = self.resolve(ci, cj)
                if resolvent is not None:
                    if len(resolvent) == 0:
                        return True  # Return True (unsatisfiable)
                    new.add(resolvent)

            if new.issubset(clauses):
                return False  # Return False (satisfiable)
            clauses.update(new)
            clauses_list = list(clauses)

    def negate_literal(self, literal):
        if literal.startswith("~"):
            return literal[1:]
        else:
            return f"~{literal}"
