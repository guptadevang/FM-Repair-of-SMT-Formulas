from z3 import *
from func import *
import re
import time

class MutationTesting:
    def __init__(self):
        # Initialize MutationTesting class
        
        global result
        
        # self.mutation_number = 0
        self.old_expr = []
        self.old_logical_expr = []

    
    # mutant for each unsat [a1, a4]
    def mutant_each_unsat(self, assertions, unsat_core):
        for index in unsat_core:
            print_d("\n-------------------------------")
            print_d("Unsat index:" + str(index) + "\t"+ str(assertions[index]))
            print_d("-------------------------------")
            
            # implement different mutation types
            for mutation_type in mutation_orders:
                assertion = assertions.copy()
                if mutation_type == "replace_constant":
                    print_d("*** Replace Constant Mutation ***\n")
                    self.old_expr = [] # clear the old expression
                    self.replace_constant(assertion, assertion[index][0] , index)
                    
                elif mutation_type == "replace_operator":
                    self.old_logical_expr = []
                    print_d("*** Replace Operator Mutation ***\n")
                    self.replace_operator(assertion, index)
                    
                elif mutation_type == "delete_assertion":
                    print_d("*** Delete Assertion Mutation ***\n")
                    self.delete_assertion(assertion, index)
                    
                else:
                    print_d("Unkown mutation type")
                
    
    # replace only one operator at the time 
    def replace_operator(self, assertion, unsat_index):
        
        
        # call the operator in custom order
        for op_name in operator_orders:
            asserts = assertion.copy()
            if op_name == "find_arithmetic_operators":
                print_d("** Find arithmetic method **")
                expr = asserts[unsat_index][0]
                self.find_arithmetic_operators(asserts, expr, unsat_index)
            
            elif op_name == "find_comparison_operators":
                print_d("** Find comparison method **")
                expr = asserts[unsat_index] if is_expr(asserts[unsat_index]) else asserts[unsat_index][0]
                self.find_comparison_operators(asserts, expr,unsat_index)
            
            elif op_name == "find_logical_operators":
                print_d("** Find logical method **")
                expr = asserts[unsat_index][0]
                self.find_logical_operators(asserts, expr, unsat_index)
            
            else:
                print("no operator to call")
            
    def delete_assertion(self, assertion, unsat_index):
        asserts = assertion.copy()
        print_d("Deleted Assertion index is: ",str(asserts[unsat_index]))
        asserts.pop(unsat_index)
        self.check_sat(asserts)


    def find_logical_operators(self, asserts, expr ,unsat_index):
        # print("expr : \t",expr)
        # print("is const: \t",is_const(expr))
        # print("is var: \t",is_var(expr))
        # Base case: if the expression is a constant or a simple variable, return
        if  is_const(expr) or is_var(expr) :
            return 
        # print("-----------------")
        self.old_logical_expr.append(expr)
        # print('length old_logical_expr is:\t',len(self.old_logical_expr)-1)
        # for old in self.old_logical_expr:
        #     print("old is ",old)
        # print("\n")
        
        # Check if the expression is an arithmetic operator
        if expr.decl().kind() in [Z3_OP_AND, Z3_OP_OR, Z3_OP_NOT]:
            print_d("Found logical op:\t [", expr.decl() ,"]")
            # check for the first logical operator
            
            if (len(self.old_logical_expr) > 1):
                asserts[unsat_index] = substitute(self.old_logical_expr[0], (self.old_logical_expr[len(self.old_logical_expr)-1] , replace_logical_operators(expr) ))
            #if it is not nested expression
            else:
                asserts[unsat_index] = replace_logical_operators(expr)
            print_d("revised assertions is: ",asserts[unsat_index])
            self.check_sat(asserts)
            
        # Recursively check the arguments of the expression
        for arg in expr.children():
            self.find_logical_operators(asserts ,arg ,unsat_index)


    # replace constant
    def replace_constant(self ,asserts, expr, unsat_index):
        
        
        
        self.old_expr.append(expr)
        # print_d("main expr is: ",expr)
        for term in expr.children():
            # print_d("term is: ",term)
            
            # if it is a unary operator like toReal(x) 
            # if term.decl().arity() == 1:  
            #     term = term.children()[0]
                # print_d("new term with arity 1: ", term)
                # print_d("is number", is_number(term))
            
            if (is_const(term) and is_number(term)): # (not a) is not allowed 
                # print_d("term inside: \t",term)
                # print_d("arity inside ", term.decl().arity())
                # print_d("inside the loop")
                if (len(self.old_expr) > 1):
                    # print("stack sizeL: ",len(self.old_expr))
                    # print_d("index 0 \t",self.old_expr[0])
                    # print_d("last -1 index is:\t", self.old_expr[len(self.old_expr)-1]);
                    
                    
                    XX = Real('X') if is_rational_value(term) else Int('X')
                    last_index = substitute(self.old_expr[len(self.old_expr)-1] ,(term, XX))
                    asserts[unsat_index] = substitute(self.old_expr[0], (self.old_expr[len(self.old_expr)-1], last_index ))
                    #if it is not nested expression
                else:
                    XX = Real('X') if is_rational_value(term) else Int('X')
                    asserts[unsat_index] = substitute(asserts[unsat_index][0], (term, XX))
                
                print_d("New Assertion is:\t",asserts[unsat_index])
                self.check_sat(asserts)    
                
                
        # end the recursion; 
        if  expr.decl().arity() == 0  :
            return
        
        # print_d("expr before recursion is: ",expr)   
        for arg in expr.children():
            self.replace_constant(asserts ,arg ,unsat_index)
        
     
    def find_arithmetic_operators(self, asserts, expr ,unsat_index):
        # Base case: if the expression is a constant or a simple variable, return
        if  expr.decl().arity() == 0 or is_const(expr)  :
            return 
        # print("-----------------")
        self.old_expr.append(expr)
        # print("expr is ",expr.decl().arity())
        # print('length old_expr is:\t',len(self.old_expr)-1)
        # for old in self.old_expr:
        #     print("old is ",old)
        # print("\n")
        
        # Check if the expression is an arithmetic operator
        if expr.decl().kind() in [Z3_OP_ADD, Z3_OP_SUB, Z3_OP_MUL, Z3_OP_DIV, Z3_OP_MOD, Z3_OP_IDIV]:
            for op in arithmetic_operators:
                if (str(expr.decl()) != op):
                    print_d("Found Operator:\t [",expr.decl(),']')
                    # print_d("operator is: ",op )
                    # replace new operator with the old one for nested expression
                    if (len(self.old_expr) > 1):
                        # print_d("index 0: ",self.old_expr[0])
                        # print_d("find: ", self.old_expr[len(self.old_expr)-1]);
                        # print_d("Default unsat index is: ",expr)
                        # print_d("operator is: ",op)
                        # print(replace_arithmetic_decl(expr, op))
                        asserts[unsat_index] = substitute(self.old_expr[0], (self.old_expr[len(self.old_expr)-1] , replace_arithmetic_decl(expr, op) ))
                    #if it is not nested expression
                    else:
                        asserts[unsat_index] = replace_arithmetic_decl(expr, op)
                    print_d("asserts[unsat_index] is:\t", asserts[unsat_index] )
                    # print("new assert is: \t",replace_arithmetic_decl(expr, op),' \n')
                    # print_d("assert is:", asserts )
                    self.check_sat(asserts)
        
        # Recursively check the arguments of the expression
        for arg in expr.children():
            self.find_arithmetic_operators(asserts ,arg ,unsat_index)

        
    def find_comparison_operators(self ,asserts, expr, unsat_index):
        # Find Comparison operator
        
        if expr.decl().arity() == 0 or is_const(expr)  :
            return
        
        if (is_comperison_operator(expr)):
            for op in comparison_operators:
                if (str(expr.decl()) != op):
                    asserts[unsat_index] = replace_comparison_decl(expr, op)
                    print_d("Comparison operators: [", op, "] " , asserts[unsat_index] )
                    self.check_sat(asserts)
        for arg in expr.children():
            self.find_comparison_operators(asserts ,arg ,unsat_index)
        
           

    # check the satisfiability
    def check_sat(self, asserts):
        if(asserts != []):
            # print_d("asserts is: ", asserts)  
            solver = Solver()
            solver.add(asserts)
            if solver.check() == sat:
                m = solver.model()
                result.append(solver)
                # self.mutation_number += 1
                # print_d("Sat and model is: \n"+ str(m))
                # print_p("Sat and New SMT-LIB formula is: \n"+ solver.to_smt2()) #sexpr
                # print_d("-----------------------------------")
            else:
                # print_d("unsat and failed to find a Model")
                print_d("************* END *************")
                
        else:
            print("No assertion to check\n")
            
        