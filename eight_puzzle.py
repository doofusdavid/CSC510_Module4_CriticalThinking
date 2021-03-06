from simpleai.search import SearchProblem, astar

INITIAL = (('1', '2', '3'), ('_', '4', '5'), ('6', '7', '8'))
GOAL = (('1', '2', '3'), ('4', '5', '6'), ('7', '8', '_'))


def find_location(puzzle, element_to_find):
    '''Find the location of a piece in the puzzle.
    Returns a tuple: row, column'''
    for ir, row in enumerate(puzzle):
        for ic, element in enumerate(row):
            if element == element_to_find:
                return ir, ic


def listit(t):
    return list(map(listit, t)) if isinstance(t, (list, tuple)) else t


def tupleit(t):
    return tuple(map(tupleit, t)) if isinstance(t, (tuple, list)) else t


class EightPuzzle(SearchProblem):
    def actions(self, state):
        empty_row, empty_col = find_location(state, '_')

        actions = []
        if empty_row > 0:
            actions.append(state[empty_row-1][empty_col])
        if empty_row < 2:
            actions.append(state[empty_row+1][empty_col])
        if empty_col > 0:
            actions.append(state[empty_row][empty_col-1])
        if empty_col < 2:
            actions.append(state[empty_row][empty_col+1])

        return actions

    def result(self, state, action):
        empty_row, empty_col = find_location(state, '_')
        new_row, new_col = find_location(state, action)

        # Swap the tile with the empty
        # first make it a list
        state_list = listit(state)
        state_list[empty_row][empty_col], state_list[new_row][new_col] = state_list[new_row][new_col], state_list[empty_row][empty_col]
        state = tupleit(state_list)

    def is_goal(self, state):
        return state == GOAL

    def heuristic(self, state):
        ''' Returns an estimate of how far to go to reach goal
        '''

        distance = 0

        for i in '12345678_':
            row, col = find_location(state, i)
            goal_row, goal_col = goal_positions[i]

            distance += abs(row - goal_row) + abs(col - goal_col)

        return distance

    def cost(self, state, action, state2):
        return 1


goal_positions = {}
for i in '12345678_':
    goal_positions[i] = find_location(listit(GOAL), i)

result = astar(EightPuzzle(INITIAL))

for action, state in result.path():
    print('Move Number: ', action)
    print(state)
