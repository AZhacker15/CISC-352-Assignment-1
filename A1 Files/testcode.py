import cagey_csp

board = (2,[(6, [(1, 1), (1, 2), (2, 1), (2, 2)], '+')])
csp, var_array = cagey_csp.cagey_csp_model(board)
print(csp)