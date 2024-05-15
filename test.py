from z3 import *
from func import *

# Read the SMT-LIB formula from a text file
file_path = './formula/formula2.txt';
with open(file_path, 'r') as file:
    formula_string = file.read()

# Call the function to extract constants with data types and assertions
constants, assertions = extract_constants_and_assertions_with_datatypes(formula_string)

# Create a solver
solver = Solver()

# Declare constants alonside their data types
context = {}
for constant, datatype in constants.items():
    context[constant] = eval(datatype)(constant) # {'x': x, 'y': y}

# Convert SMT-lib to FOL 
new_assertions = []
for assertion in assertions:
    new_assertions.append(parse_smt2_string(assertion, decls=context))

solver.add(new_assertions)

# Check for satisfiability
if solver.check() == sat:
    print("The formula is sat")
    model = solver.model()
    print("Model:")
    print(model)
else:
    
    print("The formula is unsat.")