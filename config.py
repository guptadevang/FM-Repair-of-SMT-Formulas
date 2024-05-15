
arithmetic_operators = ['+', '-', '*', '/']
comparison_operators = ['==', '>', '<', '>=', '<=']
# comparison_operators = ['<','>']
logical_operators = ['and', 'or', 'not']
mutation_orders =[]
operator_orders = []
# mutation_orders = ['replace_constant']
# operator_orders = [] #['find_arithmetic_operators', 'replace_comparison_operator', 'find_logical_operators']

result = []

# development or production
mode = "development"
dev = True
# show print only in development mode
if mode == "development":
    dev = True
else:
    dev = False    

