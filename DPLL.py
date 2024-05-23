import random
from clause import Clause

class DPLL:
    def __init__(self):
        self.output = ""
        self.assignments = {}

    def infer(self, kb, query):
        cnfClausesList = []  # Initializing an empty list to store CNF clauses
        for clause in kb:
            cnfClausesList.extend(clause.to_cnf())  # Converting each clause to CNF and adding to cnfClausesList
        negationOfQuery = Clause(f"~({query.expression})")  # Negating the query expression
        cnfClausesList.extend(negationOfQuery.to_cnf())  # Converting the negation of query to CNF and adding to cnfClausesList

        # Flatten and simplify the CNF clauses
        clauses = []
        for clause in cnfClausesList:
            clauses.append(frozenset(clause))  # Converting each clause to a frozenset and adding to clauses

        clauses = set(clauses)  # Converting clauses to a set to remove duplicate symbols

        is_satisfiable = self.dpll(clauses)  # Applying the DPLL algorithm to check satisfiability
        self.output = "NO" if is_satisfiable else "YES"  # If satisfiable, query is false (output NO); if unsatisfiable, query is true (output YES)
        return self.output  # Returning the output

    def dpll(self, formula):  # Method to implement the DPLL algorithm for satisfiability checking
        if formula == set():  # Returning True if formula has no clauses
            return True
        if frozenset() in formula:  # Returning False if formula has an empty clause
            return False
        for clause in formula:
            if len(clause) == 1:  # Checking if there is a unit clause in formula
                literal = next(iter(clause))  # Getting the literal from the unit clause
                return self.dpll(self.simplify(formula, literal))  # Recursively simplifying formula and checking satisfiability
        literal = random.choice(random.choice([list(clause) for clause in formula]))  # Choosing a random literal in the formula
        if self.dpll(self.simplify(formula, literal)):  # Recursively simplifying formula with the chosen literal and checking satisfiability
            return True
        else:
            negationLiteral = self.negate_literal(literal)  # Negating the chosen literal
            return self.dpll(self.simplify(formula, negationLiteral))  # Recursively simplifying formula with the negated literal and checking satisfiability

    def simplify(self, formula, literal):  # Method to simplify formula based on a literal
        newFormula = set()  # Initializing an empty set for the new formula
        for clause in formula:
            if literal in clause:  # Checking if the clause contains the literal
                continue  # Removing clauses that contain the literal
            negationLiteral = self.negate_literal(literal)  # Negating the literal
            newClause = {subClause for subClause in clause if subClause != negationLiteral}  # Removing the negation of literal in the clause
            newFormula.add(frozenset(newClause))  # Adding the new clause to the new formula
        return newFormula  # Returning the simplified formula

    def negate_literal(self, literal):  # Method to negate a literal
        return literal[1:] if literal.startswith("~") else f"~{literal}"
