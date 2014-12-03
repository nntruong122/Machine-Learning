from enum import Enum
from probability_distribution import EnumerationDistribution
from grid_world import *
import random, math

class Action(Enum):
    """Possible actions for grid world"""
    right = 1
    left = 2
    up = 3
    down = 4

class QLearning(object):
    """docstring for QLearning"""
    def __init__(self, grid):
        super(QLearning, self).__init__()
        if not isinstance(grid, Grid):
            raise ValueError("grid should be of type Grid")
        self.grid = grid
        self.q_values = {}
        self.actionDistributions = { Action.right : EnumerationDistribution({Action.right : 0.8, Action.down : 0.2}),
                        Action.left : EnumerationDistribution({Action.left : 1.0}),
                        Action.up : EnumerationDistribution({Action.up : 0.8, Action.left : 0.2}),
                        Action.down : EnumerationDistribution({Action.down : 1.0}) }


    def _changeState(self, currentState, desiredAction):
        if currentState.state_type == State.StateType.goal:
            # print("Returning the same state (%d, %d) : GOAL" % (currentState.row, currentState.col))
            return (currentState, random.choice(list(Action)))

        actualAction = self.actionDistributions.get(desiredAction).get_object()
        row = currentState.row
        col = currentState.col

        if actualAction == Action.right:
            nextState = self.grid.states[row][col+1] if col != self.grid.numCols-1 else currentState
        elif actualAction == Action.left:
            nextState = self.grid.states[row][col-1] if col != 0 else currentState
        elif actualAction == Action.up:
            nextState = self.grid.states[row+1][col] if row!= self.grid.numRows-1 else currentState
        else:
            nextState = self.grid.states[row-1][col] if row != 0 else currentState

        if nextState.state_type == State.StateType.unreachable:
            # print("Returning the same state (%d, %d): state (%d, %d) not reachable" % (currentState.row,
            #                                                                             currentState.col,
            #                                                                             nextState.row,
            #                                                                             nextState.col))
            return (currentState, actualAction)

        return (nextState, actualAction)

    def _generate_reachable_state(self):
        row = random.randint(0, self.grid.numRows-1)
        col = random.randint(0, self.grid.numCols-1)
        state = self.grid.states[row][col]
        while not state.is_reachable():
            state = self._generate_reachable_state()
        return state

    def learn(self, alpha = 0.1, gamma = 0.9, convergeWhen = 0):
        isConvergenceMet = False
        iterationCount = 1
        while not isConvergenceMet:
            isConvergenceMet = True
            # print("Iteration : %d" % (iterationCount))
            # currentState = nextState = self.grid.states[0][0]
            currentState = nextState = self._generate_reachable_state()
            while True:
                # print("Current state (%d, %d)" % (currentState.row, currentState.col))
                desiredAction = self.get_boltzman_action(currentState)
                nextState, actionTaken = self._changeState(currentState, desiredAction)
                currentQValue = self.q_values.get((currentState.row, currentState.col, actionTaken), 0.0)

                updatedQValue = (1 - alpha) * currentQValue
                reward = currentState.state_type.value
                maxQValueOfNextState = max(
                                            [
                                                self.q_values.get((nextState.row, nextState.col, action), 0.0)
                                                    for action in Action
                                            ]
                                          )

                noisySampleValue = alpha * (reward + gamma * maxQValueOfNextState)
                updatedQValue += noisySampleValue
                self.q_values[(currentState.row, currentState.col, actionTaken)] = updatedQValue
                if abs(updatedQValue - currentQValue) > convergeWhen * currentQValue:
                    isConvergenceMet = False
                if currentState.state_type == State.StateType.goal:
                    iterationCount += 1
                    break
                currentState = nextState
                # print("Next state (%d, %d)" % (currentState.row, currentState.col))
        self.print_q_values(iterationCount)

    def print_q_values(self, iterationCount):
        print("After %d iterations:" % (iterationCount))
        print("--------------------")
        for row in self.grid.states:
            for state in row:
                if state.is_reachable():
                    print("\nQ-values for State (%d, %d):" % (state.row, state.col))
                    print("--------------------")
                    for action in Action:
                        print("Action : %s, Q-Value : %s" %
                            (str(action),
                             str(round(self.q_values.get((state.row, state.col, action), 'UN-COMPUTED'), 2))
                            ))

    def get_boltzman_action(self, state):
        actionValueMap = {}
        for action in Action:
            q_value = self.q_values.get((state.row, state.col, action))
            # print(actionValueMap)
            actionValueMap[action] = math.exp(q_value) if q_value else 1.0

        if(len(actionValueMap) == 0):
            return random.choice(list(Action))
        else:
            return EnumerationDistribution(actionValueMap).get_object()
