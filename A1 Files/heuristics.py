# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

1. ord_dh (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Degree heuristic

2. ord_mv (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Minimum-Remaining-Value heuristic


var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    Variables and constraints of the problem. The assigned Variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return next Variable to be assigned according to the Degree Heuristic '''
    # IMPLEMENT

    max_degree = -1
    chosen_var = None

    for is_var in csp.get_all_unasgn_vars():
        degree = 0
        for con in csp.get_cons_with_var(is_var):
            for n in con.get_scope():
                if not n.is_assigned() and n != is_var:
                    degree += 1
        if degree > max_degree:
            max_degree = degree
            chosen_var = is_var

    return chosen_var


def ord_mrv(csp):
    ''' return Variable to be assigned according to the Minimum Remaining Values heuristic '''
    # IMPLEMENT

    min_domain_size = float('inf')
    chosen_var = None

    for is_var in csp.get_all_unasgn_vars():
        domain_size = is_var.cur_domain_size()
        if domain_size < min_domain_size:
            min_domain_size = domain_size
            chosen_var = is_var

    return chosen_var

