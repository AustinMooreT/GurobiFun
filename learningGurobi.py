from gurobipy import *

def powerset(s):
    """ Given a set s generates a list of all the
        subsets of the set s. """

    pset = []
    for x in s:
        newSets = []
        for originalSet in pset:
            newSet = originalSet.copy()
            newSet.add(x)
            newSets.append(newSet)
        pset = pset + newSets
        pset.append(set([x]))
    pset.append(set())
    return pset

def createSpernerModel(n):
    """ Generates a linear programming model
    for Sperner's theorm where n represents the
    size of the set. """

    model = Model("Sperner's " + str(n))

    nSet = set([x for x in range(n)])
    powerNSet = powerset(nSet)

    variables = []
    constraints = []

    # generates list of variables in model.
    # each variable is either 0 or 1.
    # each item in the list is a tuple of the form
    # (model variable, subset)
    i = 0
    for x in powerNSet:
        variables.append((model.addVar(
            vtype = GRB.BINARY,   # variable type.
            name  = "x_" + str(i) # variable name.
        ), x))
        i += 1

    # generates a list of constraints for the model.
    # each constraint is of the form x_i + x_j <= 1
    # where the tuples in variables containing x_i and x_j
    # are of the form (x_i, ss_i), (x_j, ss_j) and
    # ss_i is a subset, but not equal to ss_j.
    i = 0
    for x in variables:
        for y in variables:
            if x[1] < y[1]:
                constraints.append(model.addLConstr(
                    lhs   = x[0] + y[0],    # left hand side.
                    sense = GRB.LESS_EQUAL, # inequality.
                    rhs   = 1,              # right hand side.
                    name  = "c_" + str(i)   # constraint name.
                ))
                i += 1

    # creates objective function for the model
    # the objective function is the sum of all variables
    # in the variables list with coefficient 1.0.
    model.setObjective(
        LinExpr(list(map(lambda x : (1.0, x[0]), variables))),
        GRB.MAXIMIZE)

    return model

sp10 = createSpernerModel(10)
sp10.optimize()

