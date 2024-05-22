class DPLL:
    def __init__(self):
        self.output = ""
        self.assignments = {}

    def getOutput(self):
        return self.output

    def infer(self, kb, symbols):
        # Convert the knowledge base (kb) to Conjunctive Normal Form (CNF)
        cnf_formula = []
        for clause in kb:
            cnf_formula.extend(clause.to_cnf())
        
        # Perform DPLL recursion to check satisfiability
        result, assignments = self.dpll_recursion(cnf_formula, {})
        if result:
            # If satisfiable, set the output to "YES"
            self.output = "YES"
        return self.output

    def unit_propagation(self, formula, assignments):
        # Continue unit propagation until no more unit clauses exist
        while any(len(clause) == 1 for clause in formula):
            unit = next(clause[0] for clause in formula if len(clause) == 1) # Find the first unit clause
            formula = [clause for clause in formula if unit not in clause]# Remove clauses containing the unit
            # Remove negations of the unit from remaining clauses
            formula = [[lit for lit in clause if -unit != lit] for clause in formula] 
            assignments[abs(unit)] = True if unit > 0 else False # Update assignments based on the unit clause
        return formula, assignments

    def pure_literal_elimination(self, formula, assignments):
        all_literals = set(abs(lit) for clause in formula for lit in clause) # Get all literals in the formula

        for literal in all_literals: # Check for pure literals and update formula and assignments
            positive_literal = all(literal in clause for clause in formula if abs(literal) in clause)
            negative_literal = all(-literal in clause for clause in formula if abs(literal) in clause)

            if positive_literal:
                formula = [clause for clause in formula if literal not in clause and -literal not in clause]
                assignments[literal] = True
            elif negative_literal:
                formula = [clause for clause in formula if -literal not in clause and literal not in clause]
                assignments[literal] = False
        
        return formula, assignments # Return the updated formula and assignments

    def dpll_recursion(self, formula, assignments):
        formula, assignments = self.unit_propagation(formula, assignments) # Perform unit propagation
        
        # If formula is empty, return True and assignments (satisfiable)
        if not formula:
            return True, assignments
        # If any clause is empty, return False (unsatisfiable)
        if any(len(clause) == 0 for clause in formula):
            return False, {}
        # Perform pure literal elimination
        formula, assignments = self.pure_literal_elimination(formula, assignments)
        
        for clause in formula: # Choose a literal for branching
            if len(clause) > 0:
                literal = clause[0]
                break

        new_formula = [clause for clause in formula if literal not in clause] # Explore positive branch
        positive_branch = self.dpll_recursion(new_formula, {**assignments, abs(literal): True})
        if positive_branch[0]:
            return positive_branch
        
        new_formula = [clause for clause in formula if -literal not in clause] # Explore negative branch
        return self.dpll_recursion(new_formula, {**assignments, abs(literal): False})
