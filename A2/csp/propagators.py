# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented to complete problem solution.  

"""This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   """


def prop_BT(csp, newVar=None):
    """Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints"""

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []


def prop_FC(csp, newVar=None):
    """Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return """

    pruned_vals = []

    if not newVar:
        list = csp.get_all_cons()
    else:
        list = csp.get_cons_with_var(newVar)

    for con in list:
        if con.get_n_unasgn() == 1:
            unassigned = con.get_unasgn_vars()
            dwo, pruned = FCCheck(con, unassigned[0])
            pruned_vals += pruned

            # If there is a DWO, return it
            if dwo is True:
                return False, pruned_vals

    return True, pruned_vals


def FCCheck(c, x):
    pruned_vals = []

    # c is a constraint with all its variables already assigned, except for x
    for domain_member in x.cur_domain():
        constraint_vars = c.get_scope()
        valued_assigned = []

        # check if making x = constraint_var together with previous
        # assignments to variables in scope C falsify C
        for var in constraint_vars:
            if var == x:
                valued_assigned.append(domain_member)
            else:
                assigned_val = var.get_assigned_value()
                valued_assigned.append(assigned_val)

        if c.check(valued_assigned) is False:
            pruned_vals.append((x, domain_member))
            x.prune_value(domain_member)

        # Constraint was falsified. DWO.
        if not x.cur_domain():
            return True, pruned_vals

    return False, pruned_vals


def prop_GAC(csp, newVar=None):
    """Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue"""

    queue = []

    if not newVar:
        list = csp.get_all_cons()
    else:
        list = csp.get_cons_with_var(newVar)

    for con in list:
        queue = [con] + queue

    dwo, pruned_vals = GAC(queue, csp)

    if dwo is True:
        return False, pruned_vals

    return True, pruned_vals


def GAC(queue, csp):
    # queue contains all constraints one of whose variables has had its domain reduced.
    # At the root of search tree, first we run GAC with all contraints on queue

    pruned_vals = []
    while queue:
        c = queue.pop()
        all_constraints = c.get_scope()
        for constraint in all_constraints:
            for curr in constraint.cur_domain():

                # when a value pair does not have supporting tuple
                if c.has_support(constraint, curr) is False:

                    # append to pruned_vals list
                    # remove value from constraints
                    pruned_vals.append((constraint, curr))
                    constraint.prune_value(curr)

                    # push all constraints in scope of c but not in queue onto queue
                    # return DWO if current domain is empty
                    if constraint.cur_domain():
                        for constr in csp.get_cons_with_var(constraint):
                            if constr not in queue:
                                queue = [constr] + queue
                    else:
                        return True, pruned_vals

    return False, pruned_vals
