from z3 import *
from func import *

class Preprocessor:
    def __init__(self):
        # Initialize MutationTesting class
        asserts = [] 
        global operator_orders
        global mutation_orders
        self.operators = {}
        self.arith_op = []
        self.logic_op = []
        self.comp_op = []
        self.const_numbers = []

    def count_operators(self,expr):
        
        for arg in expr.children():
            if is_number(arg):
                self.const_numbers.append(arg)
        
        # if the expression is a constant number
        if expr.decl().arity() == 0  :
            self.operators = {tuple(self.arith_op), tuple(self.logic_op), tuple(self.comp_op), tuple(self.const_numbers)}
            return 
        
        # count arithmetic operators
        if expr.decl().kind() in [Z3_OP_ADD, Z3_OP_SUB, Z3_OP_MUL, Z3_OP_DIV, Z3_OP_MOD, Z3_OP_IDIV]:
           self.arith_op.append(expr.decl())
        
        # count logical operators
        if expr.decl().kind() in [Z3_OP_AND, Z3_OP_OR, Z3_OP_NOT]:
            self.logic_op.append(expr.decl())
            
    
        # count comparison operators
        if expr.decl().kind() in [Z3_OP_LT, Z3_OP_GT, Z3_OP_LE, Z3_OP_GE, Z3_OP_EQ]:
            self.comp_op.append(expr.decl())
        
        for arg in expr.children():
            self.count_operators( arg )


    def set_strategy(self, assertion, unsat_core):
        
        for index in unsat_core:
            # print_d("-------------------------------")
            # print_d("Unsat index:" + str(index) + "\t"+ str(assertion[index]))
            # print_d("-------------------------------")
            self.count_operators(assertion[index][0])
        
        if (self.const_numbers):    # if there is any constant number in unsat core assertion
            mutation_orders.append("replace_constant")
        if (len(assertion) > 1):    # if there is more than one assertion in unsat core
            mutation_orders.append("delete_assertion")
        if (len(self.arith_op)  > 0 or len(self.logic_op) > 0 or len(self.comp_op) > 0): # if there is any operator in unsat core assertion
            mutation_orders.append("replace_operator") 
        
        if len(self.logic_op) > 0 :
            operator_orders.append("find_logical_operators")
        
        if len(self.comp_op) > 0 :
            operator_orders.append("find_comparison_operators")
        
        if len(self.arith_op) > 0 :
            operator_orders.append("find_arithmetic_operators")
        
        print_d("**** Preprocessor ****")
        print_d("Operators in UNSAT lines only:\t", str(self.operators))
        print_d("Arithmetic operators numbers:\t", len(self.arith_op))
        print_d("Logical operators numbers:\t", len(self.logic_op))
        print_d("Comparison operators numbers:\t", len(self.comp_op))
        print_d("Constant numbers:\t", len(self.const_numbers))
        print_d("Number of assertions:\t", len(assertion))
        print_d("Mutation orders are:\t", mutation_orders)
        print_d("Operator orders are:\t", operator_orders)
        print_d("**** END ****\n")
        
    
    
        
    
    
    