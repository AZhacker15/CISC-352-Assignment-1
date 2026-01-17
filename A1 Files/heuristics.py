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
    unassigned = csp.get_all_unasgn_vars()
    if not unassigned:
        return None

    best_var = None
    best_degree = -1

    unassigned_set = set(unassigned)

    for v in unassigned:
        degree = 0
        for con in csp.get_cons_with_var(v):
            # count how many OTHER unassigned vars are in this constraint's scope
            for u in con.get_scope():
                if u is not v and u in unassigned_set:
                    degree += 1

        if degree > best_degree:
            best_degree = degree
            best_var = v

    return best_var


def ord_mrv(csp):
    ''' return Variable to be assigned according to the Minimum Remaining Values heuristic '''
    unassigned = csp.get_all_unasgn_vars()
    if not unassigned:
        return None

    # pick the variable with the smallest current domain size
    mrv_var = unassigned[0]
    min_size = mrv_var.cur_domain_size()

    for v in unassigned[1:]:
        sz = v.cur_domain_size()
        if sz < min_size:
            min_size = sz
            mrv_var = v

    return mrv_var
