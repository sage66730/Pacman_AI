# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        #util.pause()

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #print(type(newPos))
        #print(type(newFood))
        #print(type(newGhostStates))
        #print(type(newScaredTimes))
        food = currentGameState.getFood().asList()
        nearFood = min([ (f,d(f,newPos)) for f in food ], key=lambda x: x[1])
        newFood = newFood.asList()
        newGhostPos = newGhostStates[0].getPosition()
        
        ghost_dis_score = 0 if d(newGhostPos,newPos)>2 else -10000
        eat_food_score = 1000 if len(newFood)<len(food) else 0
        dir_score = -1*nearFood[1]
        #print(action, ghost_dis_score, eat_food_score, dir_score)

        return ghost_dis_score + eat_food_score + dir_score

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def maximizer(gameState, idx, depth):
            #print("maxi", depth, idx, gameState.getLegalActions(idx))
            #print("maxi", depth, idx, gameState.state, gameState.getLegalActions(idx))
            numAgents = gameState.getNumAgents()
            legalMoves = gameState.getLegalActions(idx)
            if legalMoves==[]: return self.evaluationFunction(gameState)

            scores = []
            for move in legalMoves:
                scores.append(minimizer(gameState.generateSuccessor(idx, move), (idx+1)%numAgents, depth))

            if depth==1:
                return legalMoves[ scores.index(max(scores)) ]
            else:
                return max(scores)
        
        def minimizer(gameState, idx, depth):
            #print("maxi", depth, idx, gameState.getLegalActions(idx))
            #print("mini", depth, idx, gameState.state, gameState.getLegalActions(idx))
            numAgents = gameState.getNumAgents()
            legalMoves = gameState.getLegalActions(idx)
            if legalMoves==[]: return self.evaluationFunction(gameState)

            scores = []
            for move in legalMoves:
                if depth==self.depth and idx==numAgents-1: scores.append(self.evaluationFunction(gameState.generateSuccessor(idx, move)))
                elif idx==numAgents-1: scores.append(maximizer(gameState.generateSuccessor(idx, move), (idx+1)%numAgents, depth+1))
                else:                scores.append(minimizer(gameState.generateSuccessor(idx, move), (idx+1)%numAgents, depth))

            return min(scores)

        #print("depth", self.depth)    
        #print("num", gameState.getNumAgents())
        #print(gameState.problem.evaluation)
        return maximizer(gameState, 0, 1)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def maximizer(gameState, idx, depth):
            #print("maxi", depth, idx, gameState.getLegalActions(idx))
            #print("maxi", depth, idx, gameState.state, gameState.getLegalActions(idx))
            numAgents = gameState.getNumAgents()
            legalMoves = gameState.getLegalActions(idx)
            if legalMoves==[]: return self.evaluationFunction(gameState)

            scores = []
            for move in legalMoves:
                scores.append(expectimax(gameState.generateSuccessor(idx, move), (idx+1)%numAgents, depth))

            if depth==1:
                bestScore = max(scores)
                bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
                chosenIndex = random.choice(bestIndices) # Pick randomly among the best
                return legalMoves[ chosenIndex ]
            else:
                return max(scores)
        
        def expectimax(gameState, idx, depth):
            #print("expc", depth, idx, gameState.getLegalActions(idx))
            #print("maxi", depth, idx, gameState.state, gameState.getLegalActions(idx))
            numAgents = gameState.getNumAgents()
            legalMoves = gameState.getLegalActions(idx)
            if legalMoves==[]: return self.evaluationFunction(gameState)

            scores = []
            for move in legalMoves:
                if depth==self.depth and idx==numAgents-1: scores.append(self.evaluationFunction(gameState.generateSuccessor(idx, move)))
                elif idx==numAgents-1: scores.append(maximizer(gameState.generateSuccessor(idx, move), (idx+1)%numAgents, depth+1))
                else:                scores.append(expectimax(gameState.generateSuccessor(idx, move), (idx+1)%numAgents, depth))

            return sum(scores)/len(scores)

        #print("depth", self.depth)    
        #print("num", gameState.getNumAgents())
        #print(gameState.problem.evaluation)
        return maximizer(gameState, 0, 1)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    My evalution compose 5 weighted score:
    conditional score:
        1. (scare time only) Eat ghost: It is an agressive stratrgy to prioritize killing ghosts for score
        2. (none scare time only) Distance to ghost: It is a safe strategy to not get near to ghost (near is defined as distance of  1)
    usual score:    
        1. Amount of capsules remaining
        2. Amount of food remaining
        3. Distance (maze distance) to the closest food (if there is no any food remaining, give 10000 as prize for winning)
    These 5 scores are weighted to ensure priority. For example the -10000 ensures pacman to always avoid ghost first.
    So the logic of the pacman can be described as: avoid/kill ghost > eat capsule > eat food > look for nearest food
    """
    "*** YOUR CODE HERE ***"
    pacPos = currentGameState.getPacmanPosition()
    ghostPos = currentGameState.getGhostPositions()
    food = currentGameState.getFood().asList()
    walls = currentGameState.getWalls().asList()
    caps = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]

    atGhost = [ True for g in ghostPos if d(pacPos,g)==0 ]
    nearGhost = [ True for g in ghostPos if d(pacPos,g)<=1 ]
    #nearFood = min([ (f,d(f,pacPos)) for f in food ], key=lambda x: x[1]) if food else (-10000,0)

    ghost_eat_score = -1000 if atGhost else 0 
    ghost_dis_score = -10000 if nearGhost else 0
    cap_score = -500*len(caps)
    eat_score = -100*len(food)
    dis_score = -1*D(pacPos, food, walls) if food else 10000
    #dis_score = -1*nearFood[1] 
    #print(ghost_dis_score, eat_score, dis_score)

    if scaredTimes[0] == 0:
        return ghost_dis_score + cap_score + eat_score + dis_score
    else:
        return ghost_eat_score + cap_score + eat_score + dis_score

def d(p1,p2):
    from math import sqrt
    return sqrt( (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 )

def D(pacPos, food, walls):

    stack = util.Queue()
    stack.push( [pacPos,0,[pacPos]] )

    while not stack.isEmpty():
        pos, dis, paths = stack.pop()
        if pos in food: return dis

        px = pos[0]
        py = pos[1]
        if (px-1,py) not in walls and (px-1,py) not in paths: stack.push( [(px-1,py),dis+1,paths+[(px-1,py)]] )
        if (px+1,py) not in walls and (px+1,py) not in paths: stack.push( [(px+1,py),dis+1,paths+[(px+1,py)]] )
        if (px,py-1) not in walls and (px,py-1) not in paths: stack.push( [(px,py-1),dis+1,paths+[(px,py-1)]] )
        if (px,py+1) not in walls and (px,py+1) not in paths: stack.push( [(px,py+1),dis+1,paths+[(px,py+1)]] )
        

# Abbreviation
better = betterEvaluationFunction
