class RES:
    def __init__(self):
        self.output = "" 

    def getOutput(self):
        return self.output  
    
    def infer(self, kb, query):
        cnf_formula = []  
        for clause in kb:  
            cnf_formula.extend(clause.to_cnf())  # Convert each clause to CNF and add to cnf_formula
        query_clause = query.to_cnf()  # Convert query to CNF
        cnf_formula.extend(query_clause)  # Add query CNF clause to cnf_formula

        clauses = set(frozenset(clause) for clause in cnf_formula)  # Convert CNF clauses to frozensets
        if self.resolution_algorithm(clauses):  # Call resolution algorithm with CNF clauses
            self.output = "NO"  # Set output as "NO" if resolution algorithm returns True
        else:
            self.output = "YES"  # Set output as "YES" if resolution algorithm returns False
        return self.output 

    def resolve(self, c1, c2):
        """ Attempt to resolve two clauses c1 and c2, return None if no resolution is possible. """
        for lit in c1:  # Loop through literals in c1
            if -lit in c2:  # Check if negation of literal is in c2
                # Create a new clause without the resolved literal
                new_clause = set(c1)
                new_clause.remove(lit)
                new_clause.update(c2)
                new_clause.remove(-lit)
                return frozenset(new_clause)  # Return the resolved clause as a frozenset
        return None 

    def resolution_algorithm(self, clauses):
        """ Applies the resolution algorithm on a set of clauses, returns if it's unsatisfiable. """
        new = set()  # Initialize a set to store newly derived clauses
        clauses_list = list(clauses)  # Convert set to list for indexing
        while True:
            n = len(clauses_list) 
            # Generate all pairs of clauses
            pairs = [(clauses_list[i], clauses_list[j]) for i in range(n) for j in range(i + 1, n)]  

            for (ci, cj) in pairs:  
                resolve = self.resolve(ci, cj)  # Attempt to resolve the pair of clauses
                if resolve is not None:  # If resolution is successful
                    if len(resolve) == 0:  # If an empty clause is found
                        return True  # Return True (unsatisfiable)
                    new.add(resolve)  # Add the resolved clause to the set of new clauses

            if new.issubset(clauses):  # If no new clauses are generated
                return False  # Return False (satisfiable)
            clauses.update(new)  # Update the set of clauses with new clauses
            clauses_list = list(clauses)  # Update the list of clauses with new clauses