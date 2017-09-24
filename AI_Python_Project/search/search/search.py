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
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    # We need Stack as we are implementing Depth First Search
    from util import Stack

    stack = Stack()

    # take start state and save it in source
    source = problem.getStartState()

    visited = []  # visited list to make sure, we donot explore already explored nodes

    # get children of start state and put them in Queue
    children = problem.getSuccessors(source)
    visited.append(source)  # Add start state in visited as we have explored all its successors

    for child in children:
        stack.push((child, []))     #pushing successor and path to successor in Stack

    # now take top element of Stack and apply DFS
    while not stack.isEmpty():
        top = stack.pop()               # top element of Stack
        node = top[0]
        result = top[1]
        node_pos = node[0]            # position of node
        node_dir = node[1]


        if problem.isGoalState(node_pos):
            result.append(node_dir)
            return result

        # get successors of node
        successor = []
        if not node_pos in visited:
            successor = problem.getSuccessors(node_pos)
            visited.append(node_pos)

        for succ in successor:
            succ_pos = succ[0]

            if not succ_pos in visited:         #if successor is not visited, then push it in stack:
                temp_result = [node_dir]
                temp_result = result + temp_result
                stack.push((succ, temp_result))

############################### DFS END ########################################

def breadthFirstSearch(problem):

    # We need queue as we are implementing Breadth First Search
    from util import Queue

    queue = Queue()

    # take start state and save it in source
    source = problem.getStartState()

    visited = []        # visited list to make sure, we donot explore already explored nodes

    # get initial children and put them in Queue
    children = problem.getSuccessors(source)
    visited.append(source)          # Add start state in visited as we have already explored its children

    for child in children:
        queue.push((child, []))     # pushing child and it's path to Queue

    # now take front element of Queue and apply BFS
    while not queue.isEmpty():
        top = queue.pop()       # top element of Stack
        node = top[0]
        path = top[1]
        node_pos = node[0]    # get first element row and column
        node_dir = node[1]

        # print "z:", child_pos[2]
        if (problem.isGoalState(node_pos)):
            path.append(node_dir)
            return path

        # get successor of first element
        successor = []
        if not node_pos in visited:
            successor = problem.getSuccessors(node_pos)
            visited.append(node_pos)

        for succ in successor:
            succ_pos = succ[0]

            if not succ_pos in visited:  #if succ not in parent:
                temp_result = [node_dir]
                temp_result = path + temp_result
                queue.push((succ, temp_result))
############################### BFS END ########################################

def uniformCostSearch(problem):
    # We need a priorityqueue as we are implementing uniform cost search
    from util import PriorityQueue

    pqueue = PriorityQueue()

    # take start state and save it in source
    source = problem.getStartState()

    visited = []  # visited list to make sure, we donot explore already explored nodes
    cost = {}
    # get initial children and put them in Queue
    children = problem.getSuccessors(source)
    visited.append(source)  # Add start state in visited as we have already explored its children
    cnt = 0
    for child in children:
        child_pos = child[0]
        child_val = child[2]
        cost[child_pos] = child_val
        pqueue.push((child, []), cost[child_pos])   # pushing child and it's path to PriorityQueue
        cnt = cnt + 1

    # now take top element of Stack and apply DFS
    while not pqueue.isEmpty():
        top = pqueue.pop()  # pop element with least path from the queue
        node = top[0]
        result = top[1]
        node_pos = node[0]  # get first element row and column
        node_dir = node[1]

        if problem.isGoalState(node_pos) :
            result.append(node_dir)
            return result

        # get successor of first element

        successor = []

        if node_pos not in visited:
            successor = problem.getSuccessors(node_pos)
            visited.append(node_pos)

        cnt = 0
        while cnt < len(successor):
            succ = successor[cnt]
            succ_pos = succ[0]
            succ_val = succ[2]
            cost[succ_pos] = succ_val + cost[node_pos]

            temp_result = [node_dir]
            temp_result = result + temp_result

            if not succ_pos in visited:         #if succ not in parent:
                pqueue.push((succ, temp_result), cost[succ_pos])
            cnt = cnt + 1
############################### UCS END ########################################

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    # We need priorityqueue as we are implementing aStartSearch
    from util import PriorityQueue

    pqueue = PriorityQueue()

    # take start state and save it in source
    source = problem.getStartState()

    visited = []  # visited list to make sure, we donot explore already explored nodes

    # get initial children and put them in Queue
    children = problem.getSuccessors(source)
    visited.append(source)  # Add start state in visited as we have already explored its children
    cnt = 0
    while cnt < len(children):
        child = children[cnt]
        child_pos = child[0]
        child_val = child[2]
        h_val = heuristic(child_pos, problem)
        pqueue.push((child, [], child_val), (child_val + h_val))
        cnt = cnt + 1

    # now take top element of Stack and apply DFS
    while not pqueue.isEmpty():
        top = pqueue.pop()  # pop element with least path from the queue
        node = top[0]
        result = top[1]
        path_val = top[2]
        node_pos = node[0]  # get first element row and column
        node_dir = node[1]

        if problem.isGoalState(node_pos):
            result.append(node_dir)
            return result

        # get successor of first element
        successor = []
        if not node_pos in visited:
            successor = problem.getSuccessors(node_pos)
            visited.append(node_pos)

        cnt = 0
        while cnt < len(successor):
            succ = successor[cnt]
            succ_pos = succ[0]
            succ_val = succ[2]

            if succ_pos not in visited:
                temp_result = [node_dir]
                temp_result = result + temp_result
                h_val = heuristic(succ_pos, problem)
                pqueue.push((succ, temp_result, path_val + succ_val), (path_val + succ_val + h_val))

            cnt = cnt + 1
############################### A* END ########################################

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch