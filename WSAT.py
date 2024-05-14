import random

class WalkSAT:
    def __init__(self, max_flips=10000, p=0.5):
        self.max_flips = max_flips  # Maximum number of flips allowed
        self.p = p  # Probability to choose a random assignment

    def solve(self, kb):
        # Initialize random assignment for all symbols in the knowledge base
        symbols = {symbol: random.choice([True, False]) for clause in kb for symbol in clause.get_symbols()}
        
        for i in range(self.max_flips):
            unsatisfied_clauses = [clause for clause in kb if not clause.evaluate(symbols)]
            if not unsatisfied_clauses:
                return symbols  # Return the satisfying assignment
            
            # Randomly choose one unsatisfied clause
            clause = random.choice(unsatisfied_clauses)
            if random.random() < self.p:
                # Flip a random symbol in the clause
                symbol_to_flip = random.choice(clause.get_symbols())
                symbols[symbol_to_flip] = not symbols[symbol_to_flip]
            else:
                # Flip the symbol that minimizes the number of unsatisfied clauses
                self.flip_minimizing_symbol(clause, symbols, kb)

        return None  # Return None if no solution is found

    def flip_minimizing_symbol(self, clause, symbols, kb):
        """
        Flip the symbol in the clause that results in the fewest unsatisfied clauses.
        """
        best_flip = None
        min_unsatisfied = float('inf')

        for symbol in clause.get_symbols():
            symbols[symbol] = not symbols[symbol] # Flip the symbol
            num_unsatisfied = sum(1 for c in kb if not c.evaluate(symbols)) # Count unsatisfied clauses after the flip
            symbols[symbol] = not symbols[symbol] # Revert the flip for further testing

            # Update best flip if this results in fewer unsatisfied clauses
            if num_unsatisfied < min_unsatisfied:
                min_unsatisfied = num_unsatisfied
                best_flip = symbol

        if best_flip: # Perform the best flip
            symbols[best_flip] = not symbols[best_flip]

