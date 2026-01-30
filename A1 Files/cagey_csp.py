# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all Variables in the given csp. If you are returning an entire grid's worth of Variables
they should be arranged linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional Variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 0.5/3 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
| n^2-n | n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '%' for modular addition
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from math import prod
from cspbase import *
from itertools import permutations, product
def binary_ne_grid(cagey_grid):
    ##IMPLEMENT
    pass


def nary_ad_grid(cagey_grid):
    n=cagey_grid[0]
    var_list=[]
    for r in range(1,n+1):
        for c in range(1,n+1):
            new_var=Variable(f"Cell({r},{c})", list(range(1, n+1)))
            var_list.append(new_var)        
    newCSP=CSP("nary_ad_grid",var_list)
    for r in range(1, n+1):
        rvar=var_list[(r-1)*n : r*n]
        new_constraint = Constraint(f"R({r})", rvar)
        valid_assignments = list(permutations(range(1, n+1), n))
        new_constraint.add_satisfying_tuples(valid_assignments)
        newCSP.add_constraint(new_constraint)
    
    for c in range(1, n+1):
        cvar=[var_list[(r-1)*n + (c-1)] for r in range(1, n+1)]
        new_constraint = Constraint(f"C({c})", cvar)
        valid_assignments = list(permutations(range(1, n+1), n))
        new_constraint.add_satisfying_tuples(valid_assignments)
        newCSP.add_constraint(new_constraint)
            

    return newCSP, var_list


def cagey_csp_model(cagey_grid):
    csp, variable_list = nary_ad_grid(cagey_grid)
    n, cages = cagey_grid


    var = {}
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            var[(r, c)] = variable_list[(r - 1) * n + (c - 1)]

    operation_vars = []
    for (val, cells, operation) in cages:
        if operation == "?":
            operation_d = ['+', '-', '*', '/', '%']
        else:
            operation_d = [operation]

        cell_name = ", ".join([f"Var-Cell({r},{c})" for (r, c) in cells])
        operation_var_name = f"Cage_op({val}:{operation}:[{cell_name}])"

        operation_var = Variable(operation_var_name, operation_d)
        csp.add_var(operation_var)
        operation_vars.append(operation_var)

        cage_cell_vars = [var[(r, c)] for (r, c) in cells]
        scope = cage_cell_vars + [operation_var]
        cage_constraint = Constraint(f"Cage{val, cells, operation}", scope)

        c_domain_list = [ccv.cur_domain() for ccv in cage_cell_vars]
        valid_assignment = []

        for assignment in product(*c_domain_list):
            for op in operation_d:
                if op == '+':
                    if sum(assignment) == val:
                        valid_assignment.append(assignment + (op,))

                elif op == '*':
                    if prod(assignment) == val:
                        valid_assignment.append(assignment + (op,))

                elif op == '-':
                    if any(perm[0] - sum(perm[1:]) == val for perm in permutations(assignment)):
                        valid_assignment.append(assignment + (op,))

                elif op == '/':
                    ok = False
                    for perm in permutations(assignment):
                        current = perm[0]
                        valid = True
                        for x in perm[1:]:
                            if x == 0 or (current % x != 0):
                                valid = False
                                break
                            current //= x
                        if valid and current == val:
                            ok = True
                            break
                    if ok:
                        valid_assignment.append(assignment + (op,))

                elif op == '%':
                    mod_sum = ((sum(assignment) - 1) % n) + 1
                    if mod_sum == val:
                        valid_assignment.append(assignment + (op,))

        cage_constraint.add_satisfying_tuples(valid_assignment)
        csp.add_constraint(cage_constraint)

    variable_list.extend(operation_vars)
    return csp, variable_list
