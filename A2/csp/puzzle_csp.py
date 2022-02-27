'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = caged_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the FunPuzz puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a FunPuzz grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a FunPuzz grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. caged_csp_model (worth 25/100 marks)
    - A model built using your choice of (1) binary binary not-equal, or (2)
      n-ary all-different constraints for the grid.
    - Together with FunPuzz cage constraints.

'''
from cspbase import *
import itertools


def binary_ne_grid(fpuzz_grid):
    size = fpuzz_grid[0][0]

    var_list = []
    variables = []

    cons = []
    sat_tuples = []

    # create variables for each position in the grid
    # use a 2d list variables to store all variables
    for row in range(size):
        temp = []
        for col in range(size):
            varName = 'V{row}{col}'.format(row=row + 1, col=col + 1)
            newVar = Variable(varName, list(range(1, size + 1)))
            temp.append(newVar)
            var_list.append(newVar)
        variables.append(temp)

    # create satisfying tuples list where v1 != v2
    for t in itertools.product(list(range(1, size + 1)), list(range(1, size + 1))):
        if not t[0] == t[1]:
            sat_tuples.append(t)

    # for each pair of variables, create a binary constraint and add satisfying tuples
    for i in range(size):
        for j in range(size):
            for k in range(j + 1, size):
                # constraints in each row
                con = Constraint("Row %d %d%d" % (i, j, k), [variables[i][j], variables[i][k]])
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

                # constraints in each column
                con = Constraint("Column %d %d%d" % (i, j, k), [variables[j][i], variables[k][i]])
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

    # create csp model and add constraint
    csp = CSP("binary", var_list)
    for c in cons:
        csp.add_constraint(c)

    return csp, variables


def nary_ad_grid(fpuzz_grid):
    size = fpuzz_grid[0][0]
    sat_tuples = []

    var_list = []
    variables = []

    row_vars = []
    col_vars = []
    cons = []

    # create satisfying permutation list according to the size of grids
    for permutation in itertools.permutations(list(range(1, size + 1)), size):
        sat_tuples.append(permutation)

    for i in range(size):
        row_vars.append([])
        col_vars.append([])

    # create a variable for every position on the grid
    for row in range(size):
        temp = []
        for col in range(size):
            var_name = 'V{row}{col}'.format(row=row + 1, col=col + 1)
            new_var = Variable(var_name, list(range(1, size + 1)))
            row_vars[row].append(new_var)
            col_vars[col].append(new_var)
            temp.append(new_var)
            var_list.append(new_var)

        variables.append(temp)

    for i in range(size):
        # constraints in each row
        con = Constraint("Row %d" % i, row_vars[i])
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

        # constraints in each column
        con = Constraint("Col %d" % i, col_vars[i])
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    # create csp model and add constraint
    csp = CSP("n-ary", var_list)
    for c in cons:
        csp.add_constraint(c)

    return csp, variables


def caged_csp_model(fpuzz_grid):
    num_cages = len(fpuzz_grid)
    csp, variables = binary_ne_grid(fpuzz_grid)
    cons = []

    for i in range(1, num_cages):
        cage = fpuzz_grid[i]

        # when there are only 2 items in the list
        # the first value (position of the cell) must contain the second value (target value)
        if len(cage) == 2:
            row = int(str(cage[0])[0]) - 1
            col = int(str(cage[0])[1]) - 1
            target = cage[1]
            variables[row][col] = Variable('V{row}{col}'.format(row=row + 1, col=col + 1), [target])

        # various operations
        # last index: operation
        # second to last index: result
        # other indexes: cell positions
        else:
            operation = cage[-1]
            target = cage[-2]
            cage_vars = []
            domain = []

            # find variables in current cage
            # find domain of variables for each position in the current cage
            for j in range(len(cage) - 2):
                row = int(str(cage[j])[0]) - 1
                col = int(str(cage[j])[1]) - 1
                cage_vars.append(variables[row][col])
                domain.append(variables[row][col].domain())

            con = Constraint("Cage %d" % i, cage_vars)
            prod_domain = itertools.product(*domain)
            cage_tuple = []

            for dom in prod_domain:
                # addition
                if operation == 0:
                    sum = 0
                    for num in dom:
                        sum += num

                    if sum == target:
                        cage_tuple.append(dom)

                # subtraction
                elif operation == 1:
                    for num in itertools.permutations(dom):
                        sub = num[0]
                        for n in range(1, len(num)):
                            sub -= num[n]

                        if sub == target:
                            cage_tuple.append(dom)

                # division
                elif operation == 2:
                    for num in itertools.permutations(dom):
                        quotient = num[0]
                        for n in range(1, len(num)):
                            quotient = quotient / num[n]

                        if quotient == target:
                            cage_tuple.append(dom)

                # multiplication
                elif operation == 3:
                    prod = 1
                    for num in dom:
                        prod *= num

                    if prod == target:
                        cage_tuple.append(dom)

            con.add_satisfying_tuples(cage_tuple)
            cons.append(con)

    # add constraint
    for c in cons:
        csp.add_constraint(c)

    return csp, variables
