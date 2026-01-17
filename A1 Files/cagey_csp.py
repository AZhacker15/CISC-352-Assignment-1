# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352
# cagey_csp.py
# desc:
#
from cspbase import *
from itertools import permutations, product
from math import prod
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

def binary_ne_grid(cagey_grid):
    n, cages = cagey_grid  # cages unused in this model
    dom = list(range(1, n + 1))

    # 1) Create variables in row-major order
    var_array = []
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            var_array.append(Variable(f"V{r},{c}", dom))

    csp = CSP(f"binary_ne_grid_{n}", var_array)

    # Precompute satisfying tuples for != over domain
    ne_tuples = [(a, b) for a in dom for b in dom if a != b]

    # 2) Row constraints: for each row, add binary != for every pair
    for r in range(n):
        row_vars = var_array[r * n:(r + 1) * n]
        for i in range(n):
            for j in range(i + 1, n):
                con = Constraint(f"Row{r+1}_{i+1}!={j+1}", [row_vars[i], row_vars[j]])
                con.add_satisfying_tuples(ne_tuples)
                csp.add_constraint(con)

    # 3) Column constraints: for each column, add binary != for every pair
    for c in range(n):
        col_vars = [var_array[r * n + c] for r in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                con = Constraint(f"Col{c+1}_{i+1}!={j+1}", [col_vars[i], col_vars[j]])
                con.add_satisfying_tuples(ne_tuples)
                csp.add_constraint(con)

    return csp, var_array



def nary_ad_grid(cagey_grid):
    n, _ = cagey_grid
    csp = CSP("N-ary Grid-only Cagey")

    variables = {}
    for row in range(1, n+1):
        for col in range(1, n+1):
            var = Variable(f"Cell({row},{col})", list(range(1, n+1)))
            variables[(row, col)] = var
            csp.add_var(var)
    
    # Rows
    for row in range(1, n+1):
        row_vars = [variables[(row, col)] for col in range(1, n+1)]
        constraint = Constraint(f"R({row})", row_vars)
        valid_assignments = list(permutations(range(1, n+1), n))
        constraint.add_satisfying_tuples(valid_assignments)
        csp.add_constraint(constraint)
    
    # Columns
    for col in range(1, n+1):
        col_vars = [variables[(row, col)] for row in range(1, n+1)]
        constraint = Constraint(f"C({col})", col_vars)
        valid_assignments = list(permutations(range(1, n+1), n))
        constraint.add_satisfying_tuples(valid_assignments)
        csp.add_constraint(constraint)
    
    return csp, list(variables.values())
    """
    Grid-only model using ONLY n-ary all-different constraints for each row/col.
    Returns (csp, var_array) where var_array is row-major list of cell variables.
    """
  
    """
    Full Cagey model:
      - Uses n-ary all-different for rows/cols (like nary_ad_grid)
      - Adds one operator variable per cage
      - Adds one cage constraint per cage over [op_var] + cage_cell_vars
    Returns (csp, var_array) where var_array = all cell vars (row-major) + all cage op vars.
    """
    n, cages = cagey_grid
    dom = list(range(1, n + 1))

    # --- 1) create cell vars ---
    cell_vars = []
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            cell_vars.append(Variable(f"Cell({r},{c})", dom))

    # helper to access a cell var by (r,c) where r,c are 1-based
    def get_cell(r, c):
        return cell_vars[(r - 1) * n + (c - 1)]

    # --- 2) create CSP with cell vars first ---
    csp = CSP(f"cagey_csp_model_{n}", cell_vars[:])

    # --- 3) add row/col all-different constraints ---
    ad_tuples = list(permutations(dom, n))

    for r in range(n):
        row_vars = cell_vars[r * n:(r + 1) * n]
        con = Constraint(f"RowAD({r+1})", row_vars)
        con.add_satisfying_tuples(ad_tuples)
        csp.add_constraint(con)

    for c in range(n):
        col_vars = [cell_vars[r * n + c] for r in range(n)]
        con = Constraint(f"ColAD({c+1})", col_vars)
        con.add_satisfying_tuples(ad_tuples)
        csp.add_constraint(con)

    # --- 4) cage constraints (with op variables) ---
    op_vars = []
    allowed_ops = ['+', '-', '*', '/', '%']

def cagey_csp_model(cagey_grid):
    """
    Full Cagey model:
      - Uses n-ary all-different for rows/cols (like nary_ad_grid)
      - Adds one operator variable per cage
      - Adds one cage constraint per cage over [op_var] + cage_cell_vars
    Returns (csp, var_array) where var_array = all cell vars (row-major) + all cage op vars.
    """
    n, cages = cagey_grid
    dom = list(range(1, n + 1))

    # --- 1) create cell vars ---
    cell_vars = []
    for r in range(1, n + 1):
        for c in range(1, n + 1):
            cell_vars.append(Variable(f"Cell({r},{c})", dom))

    # helper to access a cell var by (r,c) where r,c are 1-based
    def get_cell(r, c):
        return cell_vars[(r - 1) * n + (c - 1)]

    # --- 2) create CSP with cell vars first ---
    csp = CSP(f"cagey_csp_model_{n}", cell_vars[:])

    # --- 3) add row/col all-different constraints ---
    ad_tuples = list(permutations(dom, n))

    for r in range(n):
        row_vars = cell_vars[r * n:(r + 1) * n]
        con = Constraint(f"RowAD({r+1})", row_vars)
        con.add_satisfying_tuples(ad_tuples)
        csp.add_constraint(con)

    for c in range(n):
        col_vars = [cell_vars[r * n + c] for r in range(n)]
        con = Constraint(f"ColAD({c+1})", col_vars)
        con.add_satisfying_tuples(ad_tuples)
        csp.add_constraint(con)

    # --- 4) cage constraints (with op variables) ---
    op_vars = []
    allowed_ops = ['+', '-', '*', '/', '%']

    def eval_left_assoc(values, op):
        """Return op applied left-associatively, or None if invalid (e.g., division not integer)."""
        if op == '+':
            return sum(values)
        if op == '*':
            return prod(values)
        if op == '-':
            res = values[0]
            for v in values[1:]:
                res -= v
            return res
        if op == '/':
            res = values[0]
            for v in values[1:]:
                if v == 0 or res % v != 0:
                    return None
                res //= v
            return res
        return None

    def satisfies_cage(target, vals, op):
        """vals are assigned to the cage cells in some fixed order; we can permute them to satisfy."""
        m = len(vals)

        # 1-cell cage: must equal target, op can be anything valid
        if m == 1:
            return vals[0] == target

        if op == '+':
            return sum(vals) == target

        if op == '*':
            return prod(vals) == target

        if op == '%':
            # "modular addition": interpret as wrap-around on 1..n
            # result in 1..n: ((sum-1) % n) + 1
            return (((sum(vals) - 1) % n) + 1) == target

        # '-' or '/': order matters, try permutations (dedup to avoid repeats)
        for perm in set(permutations(vals, m)):
            res = eval_left_assoc(list(perm), op)
            if res is not None and res == target:
                return True
        return False

    for (target, cell_coords, op_flag) in cages:
        cage_cells = [get_cell(r, c) for (r, c) in cell_coords]

        # operator domain
        if op_flag in allowed_ops:
            op_dom = [op_flag]
        else:
            # '?' or None or anything else treated as unknown
            op_dom = allowed_ops[:]

        # operator variable name format from API
        var_refs = ", ".join([f"Var-Cell({r},{c})" for (r, c) in cell_coords])
        op_name = f"Cage_op({target}:{op_flag}:[{var_refs}])"
        op_var = Variable(op_name, op_dom)

        # add op var to CSP and to returned array
        csp.add_var(op_var)
        op_vars.append(op_var)

        # cage constraint: scope is [op_var] + cage_cells
        scope = [op_var] + cage_cells
        con = Constraint(f"CageCon({target}:{op_flag})", scope)

        sat_tuples = []
        m = len(cage_cells)

        # enumerate possible assignments to cage cell vars
        for vals in product(dom, repeat=m):
            vals_list = list(vals)
            for op in op_dom:
                if satisfies_cage(target, vals_list, op):
                    sat_tuples.append((op,) + tuple(vals_list))

        con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(con)

    # var_array: all cells (row-major) then all op vars (in cage list order)
    var_array = cell_vars + op_vars
    return csp, var_array