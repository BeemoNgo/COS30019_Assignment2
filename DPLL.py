from clause import Clause

class DPLL:
    def __init__(self):
        self.output = ""
        self.assignments = {}

    def infer(self, kb, query):
        cnf_formula = []
        for clause in kb:
            cnf_formula.extend(clause.to_cnf())

        # Negate the query and convert to CNF
        negationOfQuery = Clause(f"~({query.expression})")
        cnf_formula.extend(negationOfQuery.to_cnf())

        # Apply the DPLL algorithm to the combined formula
        result, self.assignments = self.dpll_recursion(cnf_formula, {}, set(literal for clause in cnf_formula for literal in clause))

        # Correct interpretation of the DPLL result
        self.output = "YES" if not result else "NO"  # If unsatisfiable (result is False), query is true (output YES)
        return self.output

    def dpll_recursion(self, formula, assignments, symbols):
        formula, assignments = self.unit_propagation(formula, assignments)
        formula, assignments = self.pure_literal_elimination(formula, assignments)

        if not formula:
            return True, assignments  # Satisfiable

        if [] in formula:
            return False, {}  # Unsatisfiable

        literal = self.choose_literal(formula, symbols)
        new_assignments = assignments.copy()
        new_assignments[literal] = True
        new_formula = self.simplify(formula, literal)

        result, result_assignments = self.dpll_recursion(new_formula, new_assignments, symbols)
        if result:
            return True, result_assignments

        new_assignments[literal] = False
        negationLiteral = -literal
        new_formula = self.simplify(formula, negationLiteral)

        return self.dpll_recursion(new_formula, new_assignments, symbols)

    def simplify(self, formula, literal):
        newFormula = []
        for clause in formula:
            if literal in clause:
                continue
            new_clause = [subClause for subClause in clause if subClause != -literal]
            newFormula.append(new_clause)
        return newFormula

    def unit_propagation(self, formula, assignments):
        changed = True
        while changed:
            changed = False
            unit_clauses = [clause for clause in formula if len(clause) == 1]
            for unit in unit_clauses:
                literal = unit[0]
                if literal not in assignments:
                    formula = self.simplify(formula, literal)
                    assignments[literal] = True
                    changed = True
        return formula, assignments

    def pure_literal_elimination(self, formula, assignments):
        all_literals = set(literal for clause in formula for literal in clause)
        pure_literals = {literal for literal in all_literals if -literal not in all_literals}
        for literal in pure_literals:
            formula = self.simplify(formula, literal)
            assignments[literal] = True
        return formula, assignments

    def choose_literal(self, formula, symbols):
        unassigned_symbols = symbols - set(self.assignments.keys())
        return next(iter(unassigned_symbols)) if unassigned_symbols else next(iter(symbols))

    def evaluate_clause(self, clause, assignments):
        return any(assignments.get(literal, False) for literal in clause)
