'''
SAMI GHOCHE
DEVVRET RISHI
'''
# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util
from game import Actions

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
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

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
    "*** YOUR CODE HERE ***"

    '''
    I take into account four factors, the first is the game score
    The second is a variant of the distance to the nearest food
    The third is incentivizing eating food when possible
    The fourth is a penchant for avoiding STOP directions and idleness
    '''
    # Useful information you can extract from a GameState (pacman.py)
    # successorGameState = currentGameState.generatePacmanSuccessor(action)
    # newPos = successorGameState.getPacmanPosition()
    # newFood = successorGameState.getFood()
    # newGhostStates = successorGameState.getGhostStates()
    # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # # returns the opposite of the minimum between the nearest food and 50
    # def mindistance():
    #   distances = []
    #   for food in newFood.asList():
    #     distances.append(util.manhattanDistance(newPos, food))
    #   if distances == []:
    #     return 50
    #   return -min(min(distances), 50)

    # # return points for eating food
    # def eatingscore():
    #   if len(currentGameState.getFood().asList()) > len(newFood.asList()):
    #     return 1
    #   return 0
    
    # # penalize idleness
    # def stopscore():  
    #   if action == Directions.STOP:
    #     return -1
    #   return 0
    
    # return 2*successorGameState.getScore() + 5*mindistance() + 100*eatingscore() + 10*stopscore()

    pos = currentGameState.getPacmanPosition()
    def mindistance():
      minimum = float("inf")
      for ghostposition in currentGameState.getGhostPositions():
        minimum = min(minimum, state.dist[(pos, ghostposition)])
      return min(minimum, 50)
    print "this happened"
    return 10*currentGameState.getScore() + 50*mindistance()


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

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    '''
    Standard minimax algorithm but the minvalue function that an additonal
    argument for the ghostagent, the last ghostagent calls maxValue and 
    all other ghostagents call minvalue again
    We only go deeper when the last ghostagent calls maxValue
    '''
    def maxValue(state, depth):
      if depth == 0 or state.isWin() or state.isLose():
        return self.evaluationFunction(state)
      v = float("-inf")
      legalActions = state.getLegalActions(0)
      for a in legalActions:
        v = max(v, minValue(state.generateSuccessor(0, a), depth, 1))
      return v

    def minValue(state, depth, ghostAgent):
      if depth == 0 or state.isWin() or state.isLose():
        return self.evaluationFunction(state)
      v = float("inf")
      legalActions = state.getLegalActions(ghostAgent)
      if ghostAgent == totalAgents-1:
        for a in legalActions:
          v = min(v, maxValue(state.generateSuccessor(ghostAgent, a), depth-1))
      else:
        for a in legalActions:
          v = min(v, minValue(state.generateSuccessor(ghostAgent, a), depth, ghostAgent+1))
      return v

    totalAgents = gameState.getNumAgents()
    action = Directions.STOP
    maxv = float("-inf")
    legalActions = gameState.getLegalActions(0)
    for a in legalActions:
      v = minValue(gameState.generateSuccessor(0, a), self.depth, 1)
      if maxv < v:
        maxv = v
        action = a
    return action

class MinimaxAgentSight(MultiAgentSearchAgent):
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

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    '''
    Standard minimax algorithm but the minvalue function that an additonal
    argument for the ghostagent, the last ghostagent calls maxValue and 
    all other ghostagents call minvalue again
    We only go deeper when the last ghostagent calls maxValue
    '''
    def maxValue(state, depth):
      if depth == 0 or state.isWin() or state.isLose():
        return self.evaluationFunction(state)
      v = float("-inf")
      legalActions = state.getLegalActions(0)
      for a in legalActions:
        v = max(v, minValue(state.generateSuccessor(0, a), depth, 1))
      return v

    def minValue(state, depth, ghostAgent):
      if depth == 0 or state.isWin() or state.isLose():
        return self.evaluationFunction(state)
      v = float("inf")
      legalActions = state.getLegalActions(ghostAgent)
      if ghostAgent == totalAgents-1:
        for a in legalActions:
          v = min(v, maxValue(state.generateSuccessor(ghostAgent, a), depth-1))
      else:
        for a in legalActions:
          v = min(v, minValue(state.generateSuccessor(ghostAgent, a), depth, ghostAgent+1))
      return v

    totalAgents = gameState.getNumAgents()
    action = Directions.STOP
    maxv = float("-inf")
    legalActions = gameState.getLegalActions(0)
    for a in legalActions:
      v = minValue(gameState.generateSuccessor(0, a), self.depth, 1)
      if maxv < v:
        maxv = v
        action = a
    return action    

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  '''
  Standard minimax with alpha beta pruning, again the only difference 
  is with the last ghostagent calling maxvalue and all others calling
  minvalue. Depth only changes when the last agent calls ghostagent
  '''

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    def maxValue(state, alpha, beta, depth):
      if depth == 0 or state.isWin() or state.isLose():
        # print self.evaluationFunction(state)
        return self.evaluationFunction(state)
      v = float("-inf")
      legalActions = state.getLegalActions(0)
      for a in legalActions:
        v = max(v, minValue(state.generateSuccessor(0, a), alpha, beta, depth, 1))
        if v >= beta:
          return v
        alpha = max(alpha, v)
      return v

    def minValue(state, alpha, beta, depth, ghostAgent):
      if depth == 0 or state.isWin() or state.isLose():
        return self.evaluationFunction(state)
      v = float("inf")
      legalActions = state.getLegalActions(ghostAgent)
      if ghostAgent == totalAgents-1:
        for a in legalActions:
          v = min(v, maxValue(state.generateSuccessor(ghostAgent, a), alpha, beta, depth-1))
          if v <= alpha:
            return v
          beta = min(beta, v)
      else:
        for a in legalActions:
          v = min(v, minValue(state.generateSuccessor(ghostAgent, a), alpha, beta, depth, ghostAgent+1))
          if v <= alpha:
            return v
          beta = min(beta, v)
      return v

    totalAgents = gameState.getNumAgents()
    action = Directions.STOP
    maxv = float("-inf")
    legalActions = gameState.getLegalActions(0)
    for a in legalActions:
      v = minValue(gameState.generateSuccessor(0, a), float("-inf"), float("inf"), self.depth, 1)
      if maxv < v:
        maxv = v
        action = a
    return action
    

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  '''
  Like minimax algorithm above but instead of minvalue which takes the minimum,
  maxvalue will call expvalue which returns the average score of all possible
  actions. 
  '''
  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    def maxValue(state, depth):
      if depth == 0 or state.isWin() or state.isLose():
        return self.evaluationFunction(state)
      v = float("-inf")
      legalActions = state.getLegalActions(0)
      for a in legalActions:
        v = max(v, expValue(state.generateSuccessor(0, a), depth, 1))
      return v

    def expValue(state, depth, ghostAgent):
      if depth == 0 or state.isWin() or state.isLose():
        return self.evaluationFunction(state)
      v = 0
      legalActions = state.getLegalActions(ghostAgent)
      if ghostAgent == totalAgents-1:
        for a in legalActions:
          v += maxValue(state.generateSuccessor(ghostAgent, a), depth-1)
      else:
        for a in legalActions:
          v += expValue(state.generateSuccessor(ghostAgent, a), depth, ghostAgent+1)
      return v/len(legalActions)

    totalAgents = gameState.getNumAgents()
    action = Directions.STOP
    maxv = float("-inf")
    legalActions = gameState.getLegalActions(0)
    for a in legalActions:
      v = expValue(gameState.generateSuccessor(0, a), self.depth, 1)
      if maxv < v:
        maxv = v
        action = a
    return action





def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  '''
  This is weird because I originally had a very complicated evaluation 
  function but this simple one works much better than all my other tries.
  This one just looks at two features, the game score, and a variant 
  of the distance to the closest food.
  Basically, the gamescore pushes pacman to eat food when he can, and avoid
  dying when possible, and eat ghosts when they're scared.
  The distance to the closest food incentivizes pacman to get as close
  to some source of food as possible
  By tweaking the weights of each feature, this function makes pacman survive 
  90/100 of the time, with an average score of 1200.

  Other attempts:
  Instead of using manhattan distances, I precomputed a graph that takes walls
  into account and using the Floyd Warshall algorithm, I precomputed the real
  distances between all pairs of positions, and then used those distances
  I tried giving a negative score if pacman was within 2 steps of a (scary) ghost,
  then I tried a variant with the distance to the closest ghost
  I tried incentivizing pacman to go for the big food in the bottom right and upper
  left and then once ghosts were scared, to go and eat them by having a feature that
  returned the opposite of the distance to the closest big food and another one 
  that returned the opposite of the distance to the closest scared ghost
  I also tried a feature that returned the length of the minimum spanning tree 
  containing all food and pacman's position, but that was too slow and not really
  that successful

  In the end, this was by far my best function, and when you think about it, the gamescore
  and some measure of the distance to food should contain all the information needed 
  to behave in a smart way, I just kept tweaking the weights and eventually got lucky

  '''

  pos = currentGameState.getPacmanPosition()
  def mindistance():
    minimum = float("inf")
    for ghostposition in currentGameState.getGhostPositions():
      minimum = min(minimum, util.manhattanDistance(pos, ghostposition))
    return min(minimum, 50)
  # print "this happened"
  return 10*currentGameState.getScore() + 50*mindistance()

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  '''
  Uses minimax with alpha beta pruning with depth 4, succeeds about
  30/100 of the time, with an average score of 800
  Depth 5 is even better but I'm not sure if it's too slow for your
  machines
  '''

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    def maxValue(state, alpha, beta, depth):
      if depth == 0 or state.isWin() or state.isLose():
        return better(state)
      v = float("-inf")
      legalActions = state.getLegalActions(0)
      for a in legalActions:
        v = max(v, minValue(state.generateSuccessor(0, a), alpha, beta, depth, 1))
        if v >= beta:
          return v
        alpha = max(alpha, v)
      return v

    def minValue(state, alpha, beta, depth, ghostAgent):
      if depth == 0 or state.isWin() or state.isLose():
        return better(state)
      v = float("inf")
      legalActions = state.getLegalActions(ghostAgent)
      if ghostAgent == totalAgents-1:
        for a in legalActions:
          v = min(v, maxValue(state.generateSuccessor(ghostAgent, a), alpha, beta, depth-1))
          if v <= alpha:
            return v
          beta = min(beta, v)
      else:
        for a in legalActions:
          v = min(v, minValue(state.generateSuccessor(ghostAgent, a), alpha, beta, depth, ghostAgent+1))
          if v <= alpha:
            return v
          beta = min(beta, v)
      return v

    totalAgents = gameState.getNumAgents()
    action = Directions.STOP
    maxv = float("-inf")
    legalActions = gameState.getLegalActions(0)
    for a in legalActions:
      v = minValue(gameState.generateSuccessor(0, a), float("-inf"), float("inf"), self.depth, 1)
      if maxv < v:
        maxv = v
        action = a
    return action

class OverhearingAgent(MultiAgentSearchAgent):
  def getAction(self, gameState, list_of_ghost_actions= []):
    allGhostPositions = gameState.getGhostPositions()
    speed = 1
    actionVectors = [Actions.directionToVector( a, speed ) for a in list_of_ghost_actions]
    newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
    for i in range(len(list_of_ghost_actions)):
        allGhostPositions[i] = (allGhostPositions[i][0]+actionVectors[i][0], allGhostPositions[i][1]+actionVectors[i][1])
    def mindistance(pos, ghostpositions):
      minimum = float("inf")
      for ghostposition in ghostpositions:
        minimum = min(minimum, util.manhattanDistance(pos, ghostposition))
      return min(minimum, 50)

    pos = gameState.getPacmanPosition()
    action = Directions.STOP
    maxv = float("-inf")
    legalActions = gameState.getLegalActions(0)
    for a in legalActions:
      penalty = 0

      pos = gameState.generateSuccessor(0, a).getPacmanPosition()
      mindist = mindistance(pos, allGhostPositions)
      if mindist == 0 or pos in gameState.getGhostPositions():
      mindist = mindistance(pos, allGhostPositions)
      if mindist == 0:
        penalty = -500 
      v = 10*penalty + 50*mindist
      if maxv < v:
        maxv = v
        action = a
    return action

