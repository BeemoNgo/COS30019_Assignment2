from clause import Clause

class RES:
    def __init__(self):
        self.output = ""

    def getOutput(self):
        return self.output

    def infer(self, kb, query):
        cnf_formula = []
        for clause in kb:
            cnf_formula.extend(clause.to_cnf())  # Converting each clause to CNF and adding to cnf_formula

        # Negate the query and convert it to CNF
        negated_query = Clause(f"~({query.expression})")  # Negating the query expression
        query_clause = negated_query.to_cnf()  # Converting the negated query to CNF
        cnf_formula.extend(query_clause)

        # Convert CNF clauses to frozensets for resolution
        clauses = set(frozenset(clause) for clause in cnf_formula)
        if self.resolution_algorithm(clauses):  # Checking if the resolution algorithm finds the query entailed
            self.output = "YES"  # Set output as "YES" if resolution algorithm finds unsatisfiable (entails the query)
        else:
            self.output = "NO"  # Set output as "NO" if resolution algorithm finds satisfiable (does not entail the query)
        return self.output

    def resolve(self, c1, c2):
        """ Attempt to resolve two clauses c1 and c2, return None if no resolution is possible. """
        for lit in c1:
            if self.negate_literal(lit) in c2:  # Checking if the negation of lit exists in c2
                new_clause = set(c1)  # Creating a new set with the elements of c1
                new_clause.remove(lit)  # Removing lit from the new clause
                new_clause.update(c2)  # Adding elements of c2 to the new clause
                new_clause.remove(self.negate_literal(lit))  # Removing the negation of lit from the new clause
                return frozenset(new_clause)
        return None

    def resolution_algorithm(self, clauses):
        """ Applies the resolution algorithm on a set of clauses, returns if it's unsatisfiable. """
        new = set()  # Initializing an empty set for new clauses
        clauses_list = list(clauses)  # Converting the set of clauses to a list
        while True:
            n = len(clauses_list)  # Getting the length of the list of clauses
            pairs = [(clauses_list[i], clauses_list[j]) for i in range(n) for j in range(i + 1, n)]  # Creating pairs of clauses

            for (ci, cj) in pairs:  # Looping through pairs of clauses
                resolvent = self.resolve(ci, cj)  # Resolving the pair of clauses
                if resolvent is not None:  # Checking if resolution is successful
                    if len(resolvent) == 0:  # Checking if the resolvent is an empty clause (unsatisfiable)
                        return True  # Return True (unsatisfiable)
                    new.add(resolvent)  # Adding the resolvent to the set of new clauses

            if new.issubset(clauses):  # Checking if all new clauses are already in the set of clauses
                return False  # Return False (satisfiable)
            clauses.update(new)
            clauses_list = list(clauses)  # Converting the updated set of clauses to a list

    def negate_literal(self, literal):  # Method to negate a literal
        if literal.startswith("~"):  # Checking if the literal starts with "~"
            return literal[1:]  # Returning the literal without the negation symbol
        else:
            return f"~{literal}"  # Adding a negation symbol to the literal if it doesn't have one
