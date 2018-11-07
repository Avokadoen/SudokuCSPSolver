#!/usr/bin/python

import copy
import itertools

class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

    def add_variable(self, name, domain):
        """Add a new variable to the CSP. 'name' is the variable name
        and 'domain' is a list of the legal values for the variable.
        """
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def get_all_possible_pairs(self, a, b):
        """Get a list of all possible pairs (as tuples) of the values in
        the lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.
        """
        return itertools.product(a, b)

    def get_all_arcs(self):
        """Get a list of all arcs/constraints that have been defined in
        the CSP. The arcs/constraints are represented as tuples (i, j),
        indicating a constraint between variable 'i' and 'j'.
        """
        return [ (i, j) for i in self.constraints for j in self.constraints[i] ]

    def get_all_neighboring_arcs(self, var):
        """Get a list of all arcs/constraints going to/from variable
        'var'. The arcs/constraints are represented as in get_all_arcs().
        """
        return [ (i, var) for i in self.constraints[var] ]

    def add_constraint_one_way(self, i, j, filter_function):
        """Add a new constraint between variables 'i' and 'j'. The legal
        values are specified by supplying a function 'filter_function',
        that returns True for legal value pairs and False for illegal
        value pairs. This function only adds the constraint one way,
        from i -> j. You must ensure that the function also gets called
        to add the constraint the other way, j -> i, as all constraints
        are supposed to be two-way connections!
        """
        if not j in self.constraints[i]:
            # First, get a list of all possible pairs of values between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = filter(lambda value_pair: filter_function(*value_pair), self.constraints[i][j])

    def add_all_different_constraint(self, variables):
        """Add an Alldiff constraint between all of the variables in the
        list 'variables'.
        """
        for (i, j) in self.get_all_possible_pairs(variables, variables):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)

    def backtracking_search(self):
        """This functions starts the CSP solver and returns the found
        solution.
        """
        # reset mesure of performance
        self.backtrackCalls = 0
        self.backtrackFails = 0

        # Make a so-called "deep copy" of the dictionary containing the
        # domains of the CSP variables. The deep copy is required to
        # ensure that any changes made to 'assignment' does not have any
        # side effects elsewhere.
        assignment = copy.deepcopy(self.domains)

        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        self.inference(assignment, self.get_all_arcs())

        # Call backtrack with the partial assignment 'assignment'
        return self.backtrack(assignment)


    """The function 'Backtrack' from the pseudocode in the
    textbook.

    The function is called recursively, with a partial assignment of
    values 'assignment'. 'assignment' is a dictionary that contains
    a list of all legal values for the variables that have *not* yet
    been decided, and a list of only a single value for the
    variables that *have* been decided.

    When all of the variables in 'assignment' have lists of length
    one, i.e. when all variables have been assigned a value, the
    function should return 'assignment'. Otherwise, the search
    should continue. When the function 'inference' is called to run
    the AC-3 algorithm, the lists of legal values in 'assignment'
    should get reduced as AC-3 discovers illegal values.

    IMPORTANT: For every iteration of the for-loop in the
    pseudocode, you need to make a deep copy of 'assignment' into a
    new variable before changing it. Every iteration of the for-loop
    should have a clean slate and not see any traces of the old
    assignments and inferences that took place in previous
    iterations of the loop.
	"""

    def backtrack(self, assignment):
		self.backtrackCalls += 1
		var = self.select_unassigned_variable(assignment)
		if var == "done":
			return assignment

		for value in assignment[var]:
			currentAssignment = copy.deepcopy(assignment)

			consistent = True
			for i, j in self.constraints[var].items():
				if(len(currentAssignment[i]) == 1 and [value] == currentAssignment[i]):
					consistent = False
					break

			if consistent == True:
				currentAssignment[var] = [value]
				backUp = currentAssignment
				currentAssignment, infer = self.inference(currentAssignment, self.get_all_neighboring_arcs(var))

				if infer != False:
					result = self.backtrack(currentAssignment)
					if result != "failure":
						self.backtrackFails += 1
						return result
				else:
					currentAssignment = backUp

		return "failure"

    def backtrack_performance(self):
        print("\nbacktrack was called %d time(s)" % self.backtrackCalls)
        print("backtrack failed %d time(s)\n" % self.backtrackFails)


    def select_unassigned_variable(self, assignment):
		for i in assignment:
			if len(assignment[i]) > 1:
				return i

		return "done"


    def inference(self, assignment, queue):
		queulen = len(queue)
		count = 0
		reviseAssignment = assignment
		while queue:
			count += 1
			neighbourIJ = queue.pop(0)
			backUp = reviseAssignment
			reviseAssignment, revise  = self.revise(reviseAssignment, neighbourIJ[0], neighbourIJ[1])
			if revise != False:
				assignment = reviseAssignment
				if len(reviseAssignment[neighbourIJ[0]]) <= 0:
					return reviseAssignment, False

				neighbourK = self.get_all_neighboring_arcs(neighbourIJ[0])
				neighbourK.remove((neighbourIJ[1], neighbourIJ[0]))
				queue += neighbourK
			else:
				reviseAssignment = backUp
		return reviseAssignment, True


    """The function 'Revise' from the pseudocode in the textbook.
    'assignment' is the current partial assignment, that contains
    the lists of legal values for each undecided variable. 'i' and
    'j' specifies the arc that should be visited. If a value is
    found in variable i's domain that doesn't satisfy the constraint
    between i and j, the value should be deleted from i's list of
    legal values in 'assignment'.
    """
    def revise(self, assignment, i, j):
		revised = False
		assignment = assignment
		for x in assignment[i]:
			xYsatisfy = False
			for y in assignment[j]:
				for constraint in self.constraints[i][j]:
					if (x, y) == constraint:
						xYsatisfy = True
						break
			if xYsatisfy == False:
				assignment[i].remove(x)
				revised = True
		if revised == True:
			return assignment, True
		else:
			return assignment, False


def create_map_coloring_csp():
    """Instantiate a CSP representing the map coloring problem from the
    textbook. This can be useful for testing your CSP solver as you
    develop your code.
    """
    csp = CSP()
    states = [ 'WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T' ]
    edges = { 'SA': [ 'WA', 'NT', 'Q', 'NSW', 'V' ], 'NT': [ 'WA', 'Q' ], 'NSW': [ 'Q', 'V' ] }
    colors = [ 'red', 'green', 'blue' ]
    for state in states:
        csp.add_variable(state, colors)
    for state, other_states in edges.items():
        for other_state in other_states:
            csp.add_constraint_one_way(state, other_state, lambda i, j: i != j)
            csp.add_constraint_one_way(other_state, state, lambda i, j: i != j)
    return csp

def create_sudoku_csp(filename):
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.
    """
    csp = CSP()
    board = map(lambda x: x.strip(), open(filename, 'r'))

    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                csp.add_variable('%d-%d' % (row, col), map(str, range(1, 10)))
            else:
                csp.add_variable('%d-%d' % (row, col), [ board[row][col] ])

    for row in range(9):
        csp.add_all_different_constraint([ '%d-%d' % (row, col) for col in range(9) ])
    for col in range(9):
        csp.add_all_different_constraint([ '%d-%d' % (row, col) for row in range(9) ])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    return csp

def print_sudoku_solution(solution):
    """Convert the representation of a Sudoku solution as returned from
    the method CSP.backtracking_search(), into a human readable
    representation.
    """
    for row in range(9):
        for col in range(9):
            print solution['%d-%d' % (row, col)][0],
            if col == 2 or col == 5:
                print '|',
        print
        if row == 2 or row == 5:
            print '------+-------+------'
