import time
import copy
from collections import defaultdict

DELAY = 0.5
MCV = 1  # Most Constrained Variable
LCV = 2  # Least Constraining Value
FORWARD_CHECKING = 3
ARC_CONSISTENCY = 4


class Csp:
    def __init__(self, variables, curr_assignments, domains, neighbors, constraints, state, filtering=None,
                 variable_ordering=None, value_ordering=None):
        self.variables = variables
        self.domains = domains  # {var1: [val1, val2, ...], ...}
        self.neighbors = neighbors  # {var1: {var2, var3, ...}, ...}
        self.constraints = constraints  # {(var1, var2): {(val1, val2), ...}, ...}
        self.curr_assignments = curr_assignments  # {var1: val1, ...}
        self.unassigned_variables = variables.copy()
        self.state = state
        for var in self.curr_assignments:
            self.state[var[0]][var[1]] = str(self.curr_assignments[var])
            self.unassigned_variables.remove(var)
        self.filtering = filtering
        self.variable_ordering = variable_ordering
        self.value_ordering = value_ordering

    def assign(self, var, value):
        self.curr_assignments[var] = value
        self.unassigned_variables.remove(var)
        self.state[var[0]][var[1]] = str(value)  # works only for number variables and is just to show the state

    # def unassign(self, var):
    #     self.unassigned_variables.append(var)
    #     self.state[var[0]][var[1]] = ''
    #     self.curr_assignments.pop(var)

    def is_consistent(self, var, value):
        pass

    def select_unassigned_variable(self):
        pass

    def order_domain_values(self, var):
        pass

    def filter_domain_values(self, var):
        if self.filtering == FORWARD_CHECKING:
            return self.forward_checking(var)
        elif self.filtering == ARC_CONSISTENCY:
            return self.ac3()
        else:
            return True

    def forward_checking(self, var):
        for neighbor in self.neighbors[var]:
            if neighbor not in self.curr_assignments:
                for val in self.domains[neighbor]:
                    if not self.is_consistent(neighbor, val):
                        self.domains[neighbor].remove(val)
                if len(self.domains[neighbor]) == 0:
                    return False
        return True

    def ac3(self):
        queue = [(var, neighbor) for var in self.variables for neighbor in self.neighbors[var]]
        while queue:
            (xi, xj) = queue.pop(0)
            if self.is_removed(xi, xj):
                if len(self.domains[xi]) == 0:
                    return False
                for neighbor in self.neighbors[xi]:
                    if neighbor != xj:
                        queue.append((neighbor, xi))
        return True

    def is_removed(self, xi, xj):
        flag = False
        for x in self.domains[xi]:
            if not self.has_support(x, xi, xj):
                self.domains[xi].remove(x)
                flag = True
        return flag

    def has_support(self, x, xi, xj):
        for y in self.domains[xj]:
            if (x, y) in self.constraints[(xi, xj)]:
                return True
        return False


counter = 0


def backtrack(csp):
    global counter
    time.sleep(DELAY)
    if len(csp.curr_assignments) == len(csp.variables):
        return csp.curr_assignments

    var = csp.select_unassigned_variable()
    orders = csp.order_domain_values(var)

    for value in orders:
        if csp.is_consistent(var, value):
            pre_csp = copy.deepcopy(csp)
            pre_csp.state = csp.state
            csp.assign(var, value)
            counter += 1
            if csp.filter_domain_values(var):
                result = backtrack(csp)
                if result is not None:
                    return result
            csp = pre_csp
            csp.state[var[0]][var[1]] = ''
    return None
