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

from cspbase import *
from itertools import permutations, combinations
def binary_ne_grid(cagey_grid):
    ##IMPLEMENT
    n, cages = cagey_grid
    bin_array = []

    for x in range(n * n):
        var = Variable(str(x), list(range(1, n + 1)))
        bin_array.append(var)

    csp = CSP("B_array", bin_array)

    for row in range(n):
        row_index = [bin_array[row * n + col] for col in range(n)]
        for varc1, varc2 in combinations(row_index, 2):
            con = Constraint(f"Row {row}", [varc1, varc2])
            allowed_row = [(right, left) for right in varc1.domain()
                           for left in varc2.domain() if right != left]
            con.add_satisfying_tuples(allowed_row)
            csp.add_constraint(con)

    for col in range(n):
        col_index = [bin_array[row * n + col] for row in range(n)]
        for varc1, varc2 in combinations(col_index, 2):
            con = Constraint(f"Col {col}", [varc1, varc2])
            allowed_col = [(right, left) for right in varc1.domain()
                           for left in varc2.domain() if right != left]
            con.add_satisfying_tuples(allowed_col)
            csp.add_constraint(con)

    return csp, bin_array


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
    ##IMPLEMENT
    pass
