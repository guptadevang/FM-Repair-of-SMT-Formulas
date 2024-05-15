from z3 import *
from lib.unsat import * 
from lib.mutation import * 
from func import *
from lib.preprocessor import *


# Read the formula from the file
try:
    file_path = './formula/formula31.txt';
    with open(file_path, 'r') as file:
        formula_string = file.read()
except Exception as e:
    print("Error in Reading file :", e , "\n")
    sys.exit()  


# Call the function to extract constants with data types and assertions
constants, SMTLIB_assertions = extract_constants_and_assertions_with_datatypes(formula_string)


# Declare constants alonside their data types
context = {}
for constant, datatype in constants.items():
    context[constant] = eval(datatype)(constant) # {'x': x, 'y': y}



# Convert SMT-LIB[QF-LIA] to FOL 
assertions = []
for SMTLIB_assertion in SMTLIB_assertions:
    try:
        assertions.append(parse_smt2_string(SMTLIB_assertion, decls=context))
    except Exception as e:
        print("\nError in parsing: ", SMTLIB_assertion, "\n", e, "\n")
        sys.exit()  


print("\nYou are in:\t", mode, "mode")
print_d("constants are:\t", context);
print_d("-------------------------------");
# Create a solver
solver = Solver()
solver.add(assertions)


# Check for satisfiability
if solver.check() == sat:
    model = solver.model()
    print("Formula is SAT and Our model is:\n",model)
    print_p("SMT-LIB formula is: \n"+ solver.to_smt2())

elif solver.check() == unsat:
    # check the unsat core
    unsat = UnsatCoreChecker()
    unsat_result = unsat.check_unsat_core(solver)
    
    # set strategy for mutation 
    preprocessor = Preprocessor()   
    preprocessor.set_strategy(assertions, unsat_result)
    
    # check UNSAT core
    print("Formula is UnSAT core at:\t"+ str(unsat_result))
    
    # check the mutation
    mutation = MutationTesting()
    mutation.mutant_each_unsat(assertions, unsat_result)
    
    # find the best model Base on Time and memory
    print('\n************************* Best Model *************************')
    print("Total number of solution: \t", len(result))
    model = find_best_model()
    print("The Best Model Based on Less Time and Memory is: \n\n",result[model[0][0]].to_smt2())
    print('***************************** End ****************************')

else:
    print("The formula is unknown.") 
