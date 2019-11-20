# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """

    frontier = util.Stack()
    explored = []
    frontier.push([(problem.getStartState(), 'Stop', 0)])

    while not frontier.isEmpty():
        path = frontier.pop()

        """
        If we reached the goal, then return the actions of every state in the path,
        starting from the first move.
        """
        lastState = path[-1][0]
        if problem.isGoalState(lastState):
            return [x[1] for x in path][1:]

        if lastState not in explored:
            explored.append(lastState)

            """
            For every successor state, in E, W, S, N order, check that the state has not been explored yet.
            If ok, then update the path and add it in the frontier.
            """
            for successor in problem.getSuccessors(lastState)[::-1]:
                if successor[0] not in explored:
                    newPath = path[:]
                    newPath.append(successor)
                    frontier.push(newPath)
    return []


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    frontier = util.Queue()
    explored = []
    frontier.push([(problem.getStartState(), 'Stop', 0)])

    while not frontier.isEmpty():
        path = frontier.pop()

        """
        If we reached the goal, then return the actions of every state in the path,
        starting from the first move.
        """
        lastState = path[-1][0]
        if problem.isGoalState(lastState):
            return [x[1] for x in path][1:]

        if lastState not in explored:
            explored.append(lastState)

            """
            For every successor state, in E, W, S, N order, check that the state has not been explored yet.
            If ok, then update the path and add it in the frontier.
            """
            for successor in problem.getSuccessors(lastState)[::-1]:
                if successor[0] not in explored:
                    newPath = path[:]
                    newPath.append(successor)
                    frontier.push(newPath)
    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    frontier = util.PriorityQueueWithFunction(lambda path: problem.getCostOfActions([x[1] for x in path][1:]))
    explored = []
    frontier.push([(problem.getStartState(), 'Stop', 0)])

    while not frontier.isEmpty():
        path = frontier.pop()

        """
        If we reached the goal, then return the actions of every state in the path,
        starting from the first move.
        """
        lastState = path[-1][0]
        if problem.isGoalState(lastState):
            return [x[1] for x in path][1:]

        if lastState not in explored:
            explored.append(lastState)

            """
            For every successor state, in E, W, S, N order, check that the state has not been explored yet.
            If ok, then update the path and add it in the frontier.
            """
            for successor in problem.getSuccessors(lastState)[::-1]:
                if successor[0] not in explored:
                    newPath = path[:]
                    newPath.append(successor)
                    frontier.push(newPath)
    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    start = problem.getStartState()

    dx = abs(start[0] - state[0])
    dy = abs(start[1] - state[1])

    manhattan = dx + dy
    if problem.isGoalState(state):
        return 0
    else:
        return manhattan


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    frontier = util.PriorityQueueWithFunction(lambda path: problem.getCostOfActions([x[1] for x in path][1:])
                                                           + heuristic(path[-1][0], problem))
    explored = []
    frontier.push([(problem.getStartState(), 'Stop', 0)])

    while not frontier.isEmpty():
        path = frontier.pop()

        """
        If we reached the goal, then return the actions of every state in the path,
        starting from the first move.
        """
        lastState = path[-1][0]
        if problem.isGoalState(lastState):
            return [x[1] for x in path][1:]

        if lastState not in explored:
            explored.append(lastState)

            """
            For every successor state, in E, W, S, N order, check that the state has not been explored yet.
            If ok, then update the path and add it in the frontier.
            """
            for successor in problem.getSuccessors(lastState)[::-1]:
                if successor[0] not in explored:
                    newPath = path[:]
                    newPath.append(successor)
                    frontier.push(newPath)
    return []

def aStarQuadTreeSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    solution = []
    frontier = util.PriorityQueueWithFunction(lambda path: problem.getCostOfActions([x[1] for x in path][1:])
                                                           + heuristic(path[-1][0], problem))
    explored = []
    frontier.push([(problem.getStartState(), 'Stop', 0)])

    while not frontier.isEmpty():
        path = frontier.pop()

        """
        If we reached the goal, then return the actions of every state in the path,
        starting from the first move.
        """
        lastState = path[-1][0]
        if problem.isGoalState(lastState):
            solution = [x[1] for x in path][1:]
            break

        if lastState not in explored:
            explored.append(lastState)

            """
            For every successor state, in E, W, S, N order, check that the state has not been explored yet.
            If ok, then update the path and add it in the frontier.
            """
            for successor in problem.getSuccessors(lastState):
                if successor[0] not in explored:
                    newPath = path[:]
                    newPath.append(successor)
                    frontier.push(newPath)

    print "Solution: ", solution
    return solution


def randomSearch(problem):
    import random
    current = problem.getStartState()
    solution = []
    while not (problem.isGoalState(current)):
        succ = problem.getSuccessors(current)
        no_of_successors = len(succ)
        random_succ_index = int(random.random() * no_of_successors)
        next = succ[random_succ_index]
        current = next[0]
        solution.append(next[1])
    return solution

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
rs = randomSearch
astarqt = aStarQuadTreeSearch
