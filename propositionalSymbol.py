class PropositionalSymbol:
    def __init__(self, symbol, value=None):
        self.symbol = symbol.strip()  # Remove whitespace from the symbol
        self.value = value           # Boolean value of the symbol, initially set to None

    def get_value(self):
        """
        Returns the current truth value of the propositional symbol.
        """
        return self.value

    def __str__(self):
        """
        Provides a string representation of the propositional symbol.
        """
        return self.symbol

    def __eq__(self, other):
        """
        Checks equality based on the symbol's name.
        This assumes that 'other' is another instance of PropositionalSymbol.
        """
        if isinstance(other, PropositionalSymbol):
            return self.symbol == other.symbol
        return False

    def set_propositional_symbol(self, model):
        """
        Updates the symbol's value based on a provided model.
        The model should be a dictionary where keys are symbol names and values are their truth values.
        """
        if self.symbol in model:
            self.value = model[self.symbol]