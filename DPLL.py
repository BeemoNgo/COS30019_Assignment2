import random
from clause import Clause

class DPLL:
    def __init__(self):
        self.output = ""
        self.assignments = {}

    def infer(self, kb, query):
        cnfClausesList = []
        for clause in kb:
            cnfClausesList.extend(clause.to_cnf())  # convert clause to cnf
        negationOfQuery = Clause(f"~({query.expression})")
        cnfClausesList.extend(negationOfQuery.to_cnf())  # convert negation of query to CNF

        # Flatten and simplify the CNF clauses
        clauses = []
        for clause in cnfClausesList:
            clauses.append(frozenset(clause))

        clauses = set(clauses)  # By making clauses a set, we can remove duplicate symbols

        is_satisfiable = self.dpll(clauses)
        self.output = "NO" if is_satisfiable else "YES"  # If satisfiable, query is false (output NO); if unsatisfiable, query is true (output YES)
        return self.output

    def dpll(self, formula):
        if formula == set():  # return true if formula has no clause
            return True
        if frozenset() in formula:  # return false if formula has an empty clause
            return False
        for clause in formula:
            if len(clause) == 1:  # check if there is a unit clause in formula
                literal = next(iter(clause))
                return self.dpll(self.simplify(formula, literal))
        literal = random.choice(random.choice([list(clause) for clause in formula]))  # choose a random literal in the formula
        if self.dpll(self.simplify(formula, literal)):
            return True
        else:
            negationLiteral = self.negate_literal(literal)
            return self.dpll(self.simplify(formula, negationLiteral))

    def simplify(self, formula, literal):
        newFormula = set()
        for clause in formula:
            if literal in clause:
                continue  # remove clauses that contain the literal
            # remove the negation of literal in the clauses
            negationLiteral = self.negate_literal(literal)
            newClause = {subClause for subClause in clause if subClause != negationLiteral}
            newFormula.add(frozenset(newClause))
        return newFormula

    def negate_literal(self, literal):
        return literal[1:] if literal.startswith("~") else f"~{literal}"
