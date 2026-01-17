# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352
# propagators.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

    1. prop_FC (worth 0.5/3 marks)
        - a propagator function that propagates according to the FC algorithm that 
          check constraints that have exactly one Variable in their scope that has 
          not assigned with a value, and prune appropriately

    2. prop_GAC (worth 0.5/3 marks)
        - a propagator function that propagates according to the GAC algorithm, as 
          covered in lecture

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned Variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned Variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any Variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of Variable values pairs are all of the values
      the propagator pruned (using the Variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a Variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining Variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one Variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a Variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned Variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check_tuple(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated Variable. Remember to keep
       track of all pruned Variable,value pairs and return '''
    pruned = []

    if newVar is None:
        constraints = csp.get_all_cons()
    else:
        constraints = csp.get_cons_with_var(newVar)

    for con in constraints:
        if con.get_n_unasgn() == 1:
            uvar = con.get_unasgn_vars()[0]

            # Iterate over a COPY because we may prune while iterating
            for val in list(uvar.cur_domain()):
                # check_var_val: is there still support in the constraint if uvar=val?
                if not con.check_var_val(uvar, val):
                    uvar.prune_value(val)
                    pruned.append((uvar, val))

            # Dead-end if domain wiped out
            if uvar.cur_domain_size() == 0:
                return False, pruned

    return True, pruned

            




def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated Variable. Remember to keep
       track of all pruned Variable,value pairs and return '''
    pruned = []

    if newVar is None:
        constraints = csp.get_all_cons()
    else:
        constraints = csp.get_cons_with_var(newVar)

    for con in constraints:
        if con.get_n_unasgn() == 1:
            uvar = con.get_unasgn_vars()[0]

            # Iterate over a COPY because we may prune while iterating
            for val in list(uvar.cur_domain()):
                # check_var_val: is there still support in the constraint if uvar=val?
                if not con.check_var_val(uvar, val):
                    uvar.prune_value(val)
                    pruned.append((uvar, val))

            # Dead-end if domain wiped out
            if uvar.cur_domain_size() == 0:
                return False, pruned

    return True, pruned

            




def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
       
    pruned = []

    # 1) 初始化 GAC 队列
    if newVar is None:
        gac_queue = deque(csp.get_all_cons())
    else:
        gac_queue = deque(csp.get_cons_with_var(newVar))

    # 用 id 去重：不依赖 Constraint 可 hash
    in_queue = set(id(c) for c in gac_queue)

    # 2) 处理队列
    while gac_queue:
        con = gac_queue.popleft()
        in_queue.discard(id(con))

        # 对该约束作用域内每个变量做“删无支持值”
        for var in con.get_scope():
            # 注意：遍历时拷贝一份，否则 prune 会影响迭代
            for val in list(var.cur_domain()):
                # check_var_val: “若 var=val，是否仍存在满足元组（基于当前域）”
                if not con.check_var_val(var, val):
                    # 避免重复记录（有些框架会重复调用 prune）
                    if var.in_cur_domain(val):
                        var.prune_value(val)
                        pruned.append((var, val))

                    # 域空 => 失败
                    if var.cur_domain_size() == 0:
                        return False, pruned

                    # var 域变了：所有包含 var 的约束都可能受影响，入队
                    for con2 in csp.get_cons_with_var(var):
                        if id(con2) not in in_queue:
                            gac_queue.append(con2)
                            in_queue.add(id(con2))

    return True, pruned