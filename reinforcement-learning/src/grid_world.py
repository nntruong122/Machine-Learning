from enum import Enum

class State(object):
    """Represents a position on the grid and meta information"""

    def check_positive_integer(self, variable, message):
        if not isinstance(variable, int) or variable < 0:
            raise ValueError(message)

    class StateType(Enum):
        unreachable = 0
        normal = -1
        pit = -50
        goal = 10

    def __str__(self):
        return "Row : %d, Col : %d, Type : %s" % (self.row, self.col, str(self.state_type))

    def __init__(self, row, col, state_type = StateType.normal):
        self.check_positive_integer(row, "Positive integer expected for row")
        self.check_positive_integer(col, "Positive integer expected for col")
        self.row = row
        self.col = col
        self.state_type = state_type

class Grid(object):
    """Grid world represents a grid with states and actions.
    """

    def check_positive_integer(self, variable, message):
        if not isinstance(variable, int) or variable < 0:
            raise ValueError(message)

    def is_valid_state_tuple(self, state_tuple):
        row, col = state_tuple
        return (isinstance(state_tuple, tuple)
            and row >= 0 and col >= 0
            and row < self.numRows and col < self.numCols)

    def get_state_from_tuple(self, state_tuple):
        if not self.is_valid_state_tuple(state_tuple):
            raise ValueError("Invalid tuple %s", str(state_tuple))
        row, col = state_tuple
        return self.states[row][col]

    def update_state_type(self, state_tuple, state_type):
        row, col = state_tuple
        if self.is_valid_state_tuple(state_tuple) and isinstance(state_type, State.StateType):
            self.states[row][col].state_type = state_type

    def __init__(self, numRows, numCols, unreachableTupleList, pitTupleList, goalTuple):
        super(Grid, self).__init__()
        self.check_positive_integer(numRows, "Positive integer expected for number of rows")
        self.check_positive_integer(numCols, "Positive integer expected for number of cols")

        self.numRows = numRows
        self.numCols = numCols

        if not isinstance(unreachableTupleList, list):
            raise ValueError("Unreachable tuples should be input in the form of list.")
        if not isinstance(pitTupleList, list):
            raise ValueError("Pit tuples should be input in the form of list.")
        if goalTuple[0] >= numRows or goalTuple[1] >= numCols:
            raise ValueError("Invalid goal state")

        self.states = [[State(row, col) for col in range(numCols)] for row in range(numRows)]

        for state_tuple in unreachableTupleList:
            self.update_state_type(state_tuple, State.StateType.unreachable)

        for state_tuple in pitTupleList:
            self.update_state_type(state_tuple, State.StateType.pit)

        if not self.is_valid_state_tuple(goalTuple):
            raise ValueError("Goal tuple is invalid.")
        else:
            self.update_state_type(goalTuple, State.StateType.goal)
