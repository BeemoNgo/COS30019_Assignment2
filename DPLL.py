class DPLL:
    def __init__(self):
        self.result = "NO"
        self.assignments = {}

    def infer(self, kb, symbols):
        cnf_formula = []
        for clause in kb:
            cnf_formula.extend(clause.to_cnf())
        
        result, assignments = self.dpll_recursion(cnf_formula, {})
        if result:
            self.result = "YES: " + ", ".join(f"{sym}={val}" for sym, val in assignments.items())
        return self.result

    def unit_propagation(self, formula, assignments):
        while any(len(clause) == 1 for clause in formula):
            unit = next(clause[0] for clause in formula if len(clause) == 1)
            formula = [clause for clause in formula if unit not in clause]
            formula = [[lit for lit in clause if -unit != lit] for clause in formula]
            assignments[abs(unit)] = True if unit > 0 else False
        return formula, assignments

    def pure_literal_elimination(self, formula, assignments):
        all_literals = set(abs(lit) for clause in formula for lit in clause)
        for literal in all_literals:
            positive_literal = all(literal in clause for clause in formula if abs(literal) in clause)
            negative_literal = all(-literal in clause for clause in formula if abs(literal) in clause)

            if positive_literal:
                formula = [clause for clause in formula if literal not in clause and -literal not in clause]
                assignments[literal] = True
            elif negative_literal:
                formula = [clause for clause in formula if -literal not in clause and literal not in clause]
                assignments[literal] = False
        return formula, assignments

    def dpll_recursion(self, formula, assignments):
        formula, assignments = self.unit_propagation(formula, assignments)
        
        if not formula:
            return True, assignments
        if any(len(clause) == 0 for clause in formula):
            return False, {}

        formula, assignments = self.pure_literal_elimination(formula, assignments)
        
        for clause in formula:
            if len(clause) > 0:
                literal = clause[0]
                break

        new_formula = [clause for clause in formula if literal not in clause]
        positive_branch = self.dpll_recursion(new_formula, {**assignments, abs(literal): True})
        if positive_branch[0]:
            return positive_branch
        
        new_formula = [clause for clause in formula if -literal not in clause]
        return self.dpll_recursion(new_formula, {**assignments, abs(literal): False})


