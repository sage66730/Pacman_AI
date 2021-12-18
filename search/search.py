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

from sys import path
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
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # a rahter old version search algo of mine, use a dcitionary path to record path of every point
    container = util.Stack()
    start = problem.getStartState()

    check = dict()
    path = { str(start):[] }

    container.push(start)
    
    cur = None
    while not container.isEmpty():
        #print(container.list)

        cur = container.pop()
        if not check.get(str(cur), False):
            if problem.isGoalState(cur): break

            check[str(cur)] = True

            for nm, dir, _ in problem.getSuccessors(cur): 
                if not check.get(str(nm), False): 
                    container.push(nm)
                path[str(nm)] = path[str(cur)] + [dir]
        
    return path[str(cur)]

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from searchAgents import CornersProblem

    # if the problem is corner problem =====================================================================================
    if isinstance(problem, CornersProblem):
        container = util.Queue()
        #Ans = ['West','West','West','South','South','South','South',
        #        'North','North','North','North','North',
        #        'East','East','East','East','East',
        #        'South','South','South','West','West','West','South','South','East','East','East']
        top, right = problem.walls.height-2, problem.walls.width-2
        start = problem.getStartState()
        corners = problem.foodEaten

        container.push( (start, [], [], corners) )
        
        while not container.isEmpty():
            
            cur = container.pop()
            cur_pos = cur[0]
            cur_path = cur[1]
            cur_visit = cur[2]
            cur_corn = cur[3]      

            if cur_pos not in cur_visit:
                #if cur_path == Ans[:len(cur_path)]: print("{0}th layer".format(len(cur_path)))
                    
                #if corner is visited first time clear the visited points to start a new A* search with one less corner
                if cur_pos == (1,1) and cur_corn[0] == False: 
                    cur_corn[0] = True
                    cur_visit = []
                
                if cur_pos == (1,top) and cur_corn[1] == False: 
                    cur_corn[1] = True
                    cur_visit = [] 
                
                if cur_pos == (right,1) and cur_corn[2] == False: 
                    cur_corn[2] = True
                    cur_visit = [] 
                
                if cur_pos == (right,top) and cur_corn[3] == False: 
                    cur_corn[3] = True
                    cur_visit = [] 
                
                cur_visit.append(cur_pos)
                #if cur_path == Ans[:len(cur_path)]: print(cur_corn, cur_path, cur_visit)
                
                if problem.isGoalState(cur): return cur_path

                for nm, dir, _ in problem.getSuccessors(cur_pos): 
                    container.push( (nm, cur_path+[dir], cur_visit.copy(), cur_corn.copy()) )    
        
        return []
    # if the problem is not corner problem =====================================================================================
    else:
        # a rather new version of searching algo, passing down the path with position
        container = util.Queue()
        start = problem.getStartState()

        check = dict()

        container.push((start, [], 0))
        
        while not container.isEmpty():
            #print(container.list)

            cur = container.pop()
            cur_pos = cur[0]
            cur_path = cur[1]

            if not check.get(cur_pos, False):
                if problem.isGoalState(cur_pos): return cur_path

                check[cur_pos] = True

                for nm, dir, _ in problem.getSuccessors(cur_pos): 
                        if not check.get(nm, False): 
                            container.push( (nm, cur_path+[dir]) )
            
        return []
    
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    container = util.PriorityQueue()
    start = problem.getStartState()

    check = dict()

    container.push( (start, [], 0), 0)

    cur = None
    while not container.isEmpty():

        cur = container.pop()
        cur_pos = cur[0]
        cur_path = cur[1]
        cur_cost = cur[2]

        if not check.get(cur_pos, False):
            if problem.isGoalState(cur_pos): return cur_path

            check[cur_pos] = True

            for nm, dir, cost in problem.getSuccessors(cur_pos): 
                if not check.get(nm, False): 
                    container.update((nm, cur_path+[dir], cost+cur_cost) , cost+cur_cost)
        
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from searchAgents import CornersProblem
    # if the problem is corner problem =====================================================================================
    # this piece of code take too much time as the answer lies in a deep layer (106 steps)
    # after reaching a corner, heuristic glows dramatically so priority queue has to deal with other items in queue
    if isinstance(problem, CornersProblem):
        #Ans = ['North', 'East', 'East', 'East', 'East', 'North', 'North', 'West', 'West', 'West', 'West', 'North', 'North',
        #        'North', 'North', 'North', 'North', 'North', 'North', 'West', 'West', 'West', 'West', 'South', 'South',
        #        'East', 'East', 'East', 'East', 'South', 'South', 'South', 'South', 'South', 'South', 'West', 'West',
        #        'South', 'South', 'South', 'West', 'West', 'East', 'East', 'North', 'North', 'North', 'East', 'East', 'East',
        #        'East', 'East', 'East', 'East', 'East', 'South', 'South', 'East', 'East', 'East', 'East', 'East', 'North',
        #        'North', 'East', 'East', 'North', 'North', 'East', 'East', 'North', 'North', 'East', 'East', 'East', 'East',
        #        'South', 'South', 'South', 'South', 'East', 'East', 'North', 'North', 'East', 'East', 'South', 'South',
        #        'South', 'South', 'South', 'North', 'North', 'North', 'North', 'North', 'North', 'North', 'West', 'West',
        #        'North', 'North', 'East', 'East', 'North', 'North']
        container = util.PriorityQueue()
        top, right = problem.walls.height-2, problem.walls.width-2
        start = problem.getStartState()
        corners = problem.foodEaten

        container.push( (start, [], [], corners, 0), 0 )
        
        while not container.isEmpty():

            cur = container.pop()
            cur_pos = cur[0]
            cur_path = cur[1]
            cur_visit = cur[2]
            cur_corn = cur[3]    
            cur_cost = cur[4]  

            if cur_pos not in cur_visit:
                #if cur_path == Ans[:len(cur_path)]: print("{0}th layer".format(len(cur_path)))
                    
                if cur_pos == (1,1) and cur_corn[0] == False: 
                    cur_corn[0] = True
                    cur_visit = []
                
                if cur_pos == (1,top) and cur_corn[1] == False: 
                    cur_corn[1] = True
                    cur_visit = [] 
                
                if cur_pos == (right,1) and cur_corn[2] == False: 
                    cur_corn[2] = True
                    cur_visit = [] 
                
                if cur_pos == (right,top) and cur_corn[3] == False: 
                    cur_corn[3] = True
                    cur_visit = [] 
                
                cur_visit.append(cur_pos)
                #if cur_path == Ans[:len(cur_path)]: print(cur_corn, cur_path, cur_visit)
                
                if problem.isGoalState(cur): return cur_path

                for nm, dir, cost in problem.getSuccessors(cur_pos):
                    problem.foodEaten = cur_corn 
                    container.update( (nm, cur_path+[dir], cur_visit.copy(), cur_corn.copy(), cost+cur_cost), cost+cur_cost+heuristic( nm, problem) )
                    #if cur_path == Ans[:len(cur_path)]: print("push\n", cur_corn, cur_path+[dir], cur_visit)   
        
        return []    
    # if the problem is not corner problem =====================================================================================
    else:
        container = util.PriorityQueue()
        start = problem.getStartState()

        check = dict()

        container.push( (start, [], 0), 0)

        cur = None
        while not container.isEmpty():

            cur = container.pop()
            cur_pos = cur[0]
            cur_path = cur[1]
            cur_cost = cur[2]

            if not check.get(cur_pos, False):
                if problem.isGoalState(cur_pos): return cur_path

                check[cur_pos] = True

                for nm, dir, cost in problem.getSuccessors(cur_pos): 
                    if not check.get(nm, False): 
                        container.update((nm, cur_path+[dir], cost+cur_cost) , cost+cur_cost+heuristic(nm, problem))
            
        return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
