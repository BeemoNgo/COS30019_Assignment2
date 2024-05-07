from fc import ForwardChaining
from bc import BackwardChaining
from queue import Queue

class InferenceEngine:
    def __init__(self, knowledge_base, query):
        self.knowledge_base = knowledge_base
        self.query = query
        self.true_values = Queue()
        self.facts = set()
        self.agenda = []
        self._parse_knowledge_base()

    def _parse_knowledge_base(self):
        for rule in self.knowledge_base.split(";"):
            parts = rule.strip().split("=>")
            if len(parts) == 2:
                antecedent = parts[0].strip().split("&")
                consequent = parts[1].strip()
                self.agenda.append((antecedent, consequent))
            else:
                # check if it's a single true value
                single_value = parts[0].strip()
                if single_value not in self.facts:
                    self.facts.add(single_value)
                    self.true_values.put(single_value)

    def solve(self, method):
        print("Knowledge Base:")
        print(self.knowledge_base)
        print("Query:", self.query)

        if method.upper() == "FC":
            fc = ForwardChaining(self.knowledge_base, self.query, self.true_values, self.facts, self.agenda)
            result = fc.forward_chain()
            if result:
                print("YES:", result)
                print("True values queue:")
                while not fc.true_values.empty():
                    print(fc.true_values.get(), end="; ")
            else:
                print("NO")
        elif method.upper() == "BC":
            bc = BackwardChaining(self.knowledge_base, self.query, self.true_values, self.facts, self.agenda)
            result = bc.backward_chain()
            if result:
                print("YES:", result)
                
            else:
                print("NO")

class Main: #to test without using CLI
    _KB = None                  
    _query = None                
    filename = "C:\\Users\\Hakley\\OneDrive - Swinburne University\\School Work\\SEM1_Y2\\CS30019_AI\\assignment2\\test.txt"   #pre-defined file

    def main():
        Main.read_from_file(Main.filename)
        method = "BC"       #pre-fined method
        engine = InferenceEngine(Main._KB, Main._query)
        engine.solve(method)

    def read_from_file(file_name):
        input_rows = []
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    input_rows.append(line.strip())
        except FileNotFoundError:
            print("Error: Couldn't locate file '{}'.".format(file_name))
            return False

        Main._KB = input_rows[1]
        Main._query = input_rows[3]
        return True

if __name__ == "__main__":
    Main.main()


# class Main:   #to run with CLI
#     _KB = None
#     _query = None

#     def main(args):
#         if Main.read_from_file(args[1]):      #python engine.py (text.txt) (method)
#             engine = InferenceEngine(Main._KB, Main._query)
#             method = args[2]
#             engine.solve(method)  

#     def read_from_file(file_name):
#         input_rows = []
#         try:
#             with open(file_name, 'r') as file:
#                 for line in file:
#                     input_rows.append(line.strip())
#         except FileNotFoundError:
#             print("Error: Couldn't locate file '{}'.".format(file_name))
#             return False

#         Main._KB = input_rows[1]
#         Main._query = input_rows[3]
#         return True


# if __name__ == "__main__":
#     import sys

#     Main.main(sys.argv)
