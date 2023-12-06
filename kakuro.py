from collections import defaultdict
from itertools import permutations
from csp import Csp


class Kakuro(Csp):
    def __init__(self, board, filtering=None, variable_ordering=None, value_ordering=None):
        self.board = board
        self.variables = []
        self.raw_domains = defaultdict(list)
        self.neighbors = defaultdict(set)
        self.vertical_neighbors = defaultdict(set)
        self.horizontal_neighbors = defaultdict(set)
        self.vertical_sum = defaultdict(int)
        self.horizontal_sum = defaultdict(int)
        self.constraints = defaultdict(set)
        self.curr_assignments = {}
        self.get_info(board)
        super().__init__(self.variables, self.curr_assignments, self.raw_domains, self.neighbors, self.constraints,
                         self.board, filtering, variable_ordering, value_ordering)

    def is_consistent(self, var, value):
        for neighbor in self.neighbors[var]:
            if neighbor in self.curr_assignments:
                if (self.curr_assignments[neighbor], value) not in self.constraints[(neighbor, var)]:
                    return False

        counter, sum = 0, 0
        for neighbor in self.vertical_neighbors[var]:
            if neighbor in self.curr_assignments:
                counter += 1
                sum += self.curr_assignments[neighbor]
        if (counter == len(self.vertical_neighbors[var]) and sum + value != self.vertical_sum[var]) or (
                counter != len(self.vertical_neighbors[var]) and sum + value >= self.vertical_sum[var]):
            return False

        counter, sum = 0, 0
        for neighbor in self.horizontal_neighbors[var]:
            if neighbor in self.curr_assignments:
                counter += 1
                sum += self.curr_assignments[neighbor]
        if (counter == len(self.horizontal_neighbors[var]) and sum + value != self.horizontal_sum[var]) or (
                counter != len(self.horizontal_neighbors[var]) and sum + value >= self.horizontal_sum[var]):
            return False

        return True

    def select_unassigned_variable(self):
        if self.variable_ordering != 1:
            return self.unassigned_variables[0]

        min_row_var, min_col_var, max_row_var, max_col_var = self.unassigned_variables[0], self.unassigned_variables[0], \
            self.unassigned_variables[0], self.unassigned_variables[0]

        for var in self.unassigned_variables:
            if self.horizontal_sum[var] < self.horizontal_sum[min_col_var]:
                min_col_var = var
            if self.vertical_sum[var] < self.vertical_sum[min_row_var]:
                min_row_var = var
            if self.horizontal_sum[var] > self.horizontal_sum[max_col_var]:
                max_col_var = var
            if self.vertical_sum[var] > self.vertical_sum[max_row_var]:
                max_row_var = var

        selected_vars = []

        if self.vertical_sum[min_row_var] <= self.horizontal_sum[min_col_var]:
            selected_vars.append(min_row_var)
            for n in self.vertical_neighbors[min_row_var]:
                if n in self.unassigned_variables:
                    selected_vars.append(n)
        else:
            selected_vars.append(min_col_var)
            for n in self.horizontal_neighbors[min_col_var]:
                if n in self.unassigned_variables:
                    selected_vars.append(n)

        mcv = selected_vars[0]
        for var in selected_vars:
            if len(self.domains[var]) < len(self.domains[mcv]):
                mcv = var

        return mcv

    def order_domain_values(self, var):
        values = self.domains[var].copy()

        if self.value_ordering != 2:
            return values

        def count_conflicts(value):
            conflicts = 0
            for neighbor in self.neighbors[var]:
                if neighbor in self.curr_assignments:
                    if (self.curr_assignments[neighbor], value) not in self.constraints[(neighbor, var)]:
                        conflicts += 1

            counter, sum = 0, 0
            for neighbor in self.vertical_neighbors[var]:
                if neighbor in self.curr_assignments:
                    counter += 1
                    sum += self.curr_assignments[neighbor]
            if (counter == len(self.vertical_neighbors[var]) and sum + value != self.vertical_sum[var]) or (
                    counter != len(self.vertical_neighbors[var]) and sum + value >= self.vertical_sum[var]):
                conflicts += 1

            counter, sum = 0, 0
            for neighbor in self.horizontal_neighbors[var]:
                if neighbor in self.curr_assignments:
                    counter += 1
                    sum += self.curr_assignments[neighbor]
            if (counter == len(self.horizontal_neighbors[var]) and sum + value != self.horizontal_sum[var]) or (
                    counter != len(self.horizontal_neighbors[var]) and sum + value >= self.horizontal_sum[var]):
                conflicts += 1

            return conflicts

        values.sort(key=count_conflicts)

        return values

    def get_info(self, board):
        variables = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                cell = self.board[i][j]
                if cell != 'X' and '\\' not in cell:
                    variables.append((i, j))
                    if cell != '':
                        self.curr_assignments[(i, j)] = int(cell)
                if '\\' in cell:
                    index = cell.find('\\')  # Find the index of '\\'

                    if index > 0:  # n\
                        number_before = int(cell[:index])
                        relevant_vars = []
                        k = i + 1
                        while k < len(board) and board[k][j] != 'X' and '\\' not in board[k][j]:
                            relevant_vars.append((k, j))
                            k += 1
                        self.get_info_helper(number_before, relevant_vars, is_vertical=False)

                    if index < len(cell) - 1:  # \n
                        number_after = int(cell[index + 1:])
                        relevant_vars = []
                        k = j + 1
                        while k < len(board[i]) and board[i][k] != 'X' and '\\' not in board[i][k]:
                            relevant_vars.append((i, k))
                            k += 1
                        self.get_info_helper(number_after, relevant_vars, is_vertical=True)

        self.variables = variables

    def get_info_helper(self, number_before, relevant_vars, is_vertical):
        if is_vertical:
            for var in relevant_vars:
                self.vertical_sum[var] = number_before
        else:
            for var in relevant_vars:
                self.horizontal_sum[var] = number_before

        if len(relevant_vars) == 1:
            self.raw_domains[relevant_vars[0]].append(number_before)

        dom = set()
        perms = permutations([1, 2, 3, 4, 5, 6, 7, 8, 9], len(relevant_vars))
        possible_perms = []
        for perm in perms:
            if sum(perm) == number_before:
                possible_perms.append(perm)
                for number in perm:
                    dom.add(number)
        dom = list(dom)

        for perm in possible_perms:
            for i in range(len(relevant_vars)):
                for j in range(len(relevant_vars)):
                    if i != j:
                        self.constraints[(relevant_vars[i], relevant_vars[j])].add((perm[i], perm[j]))
                        self.constraints[(relevant_vars[j], relevant_vars[i])].add((perm[j], perm[i]))

        for domain in dom:
            for var in relevant_vars:
                if var not in self.raw_domains or domain not in self.raw_domains[var]:
                    if domain <= self.horizontal_sum[var] and domain <= self.vertical_sum[var]:
                        self.raw_domains[var].append(domain)

        for v1 in relevant_vars:
            for v2 in relevant_vars:
                if v1 != v2:
                    self.neighbors[v1].add(v2)
                    self.neighbors[v2].add(v1)
                    if is_vertical:
                        self.vertical_neighbors[v1].add(v2)
                        self.vertical_neighbors[v2].add(v1)
                    else:
                        self.horizontal_neighbors[v1].add(v2)
                        self.horizontal_neighbors[v2].add(v1)
