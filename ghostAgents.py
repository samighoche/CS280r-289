# ghostAgents.py
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


from game import Agent
from game import Actions
from game import Directions
import random
from util import manhattanDistance
import util
import time

class GhostAgent( Agent ):
    def __init__( self, index ):
        self.index = index

    def getAction( self, state ):
        dist = self.getDistribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.chooseFromDistribution( dist )

    def getDistribution(self, state):
        "Returns a Counter encoding a distribution over actions from the provided state."
        util.raiseNotDefined()

class RandomGhost( GhostAgent ):
    "A ghost that chooses a legal action uniformly at random."
    def getDistribution( self, state ):
        dist = util.Counter()
        for a in state.getLegalActions( self.index ): dist[a] = 1.0
        dist.normalize()
        return dist



class FiveGhost( GhostAgent):
    "A ghost that takes into account other ghosts positions and tries to trap pacman."
    def __init__(self, index):
        self.index = index

    def count_removed_from_others(self, state, depth):
        pacmanPosition = state.getPacmanPosition()
        pos = state.getGhostPosition( self.index )
        removedPos = set()
        allGhostPositions = state.getGhostPositions()
        allGhostPositions.remove(pos)
        adj_list = state.adj_list

        walls = list(state.getWalls())
        N = len(walls)
        M = len(walls[0])

        for ghostposition in allGhostPositions:
            # check current
            if manhattanDistance(ghostposition, pacmanPosition) <= depth:
                removedPos.add(ghostposition)
            # check top
            if ghostposition[0] > 0:
                newpos = (ghostposition[0]-1, ghostposition[1])
                if manhattanDistance(newpos, pacmanPosition) <= depth:
                    removedPos.add(newpos)
            # check bottom
            if ghostposition[0] < N-1:
                newpos = (ghostposition[0]+1, ghostposition[1])
                if manhattanDistance(newpos, pacmanPosition) <= depth:
                    removedPos.add(newpos)
            # check left
            if ghostposition[1] > 0:
                newpos = (ghostposition[0], ghostposition[1]-1)
                if manhattanDistance(newpos, pacmanPosition) <= depth:
                    removedPos.add(newpos)
            if ghostposition[1] < M-1:
                newpos = (ghostposition[0], ghostposition[1]+1)
                if manhattanDistance(newpos, pacmanPosition) <= depth:
                    removedPos.add(newpos)
        return (len(removedPos), removedPos)
            


    def getDistribution(self, state, depth=6):
        speed = 1
        legalActions = state.getLegalActions( self.index )
        pos = state.getGhostPosition( self.index )
        pacmanPosition = state.getPacmanPosition()
        actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
        newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]

        

        bestNumRemoved = float("-inf")
        removedPos = set()
        bestActions = []
        walls = list(state.getWalls())
        N = len(walls)
        M = len(walls[0])
        for ghostposition in newPositions:
            numRemovedOthers, removedPos = self.count_removed_from_others(state, depth)
            if manhattanDistance(ghostposition, pacmanPosition) <= depth:
                removedPos.add(ghostposition)
            # check top
            if ghostposition[0] > 0:
                newpos = (ghostposition[0]-1, ghostposition[1])
                if manhattanDistance(newpos, pacmanPosition) <= depth:
                    removedPos.add(newpos)
            # check bottom
            if ghostposition[0] < N-1:
                newpos = (ghostposition[0]+1, ghostposition[1])
                if manhattanDistance(newpos, pacmanPosition) <= depth:
                    removedPos.add(newpos)
            # check left
            if ghostposition[1] > 0:
                newpos = (ghostposition[0], ghostposition[1]-1)
                if manhattanDistance(newpos, pacmanPosition) <= depth:
                    removedPos.add(newpos)
            if ghostposition[1] < M-1:
                newpos = (ghostposition[0], ghostposition[1]+1)
                if manhattanDistance(newpos, pacmanPosition) <= depth:
                    removedPos.add(newpos)
            if len(removedPos) - 1.5*state.dist[(ghostposition, pacmanPosition)] > bestNumRemoved:
                bestNumRemoved = len(removedPos) - 1.5*state.dist[(ghostposition, pacmanPosition)]
                action = legalActions[newPositions.index(ghostposition)]
                bestActions = [action]
            elif len(removedPos) - 1.5*state.dist[(ghostposition, pacmanPosition)] == bestNumRemoved:
                action = legalActions[newPositions.index(ghostposition)]
                bestActions.append(action)

        bestProb = 0.8

        # print bestActions
        # print len(removedPos)
        # print removedPos

        # if len(bestActions) == 1:
        #     bestActionsFinal = bestActions
        # else:
        #     actionVectors = [Actions.directionToVector( a, speed ) for a in bestActions]
        #     newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
        #     pacmanPosition = state.getPacmanPosition()

        #     # Select best actions given the state
        #     distancesToPacman = [state.dist[( pos, pacmanPosition )] for pos in newPositions]    
        #     bestScore = min( distancesToPacman )
        #     bestActionsFinal = [action for action, distance in zip( bestActions, distancesToPacman ) if distance == bestScore] 

        # print "best actions is : ", bestActions
        # print bestActionsFinal
        dist = util.Counter()
        for a in bestActions: dist[a] = bestProb / len(bestActions)
        for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
        dist.normalize()
        return dist

class DirectionalGhost( GhostAgent ):
    "A ghost that prefers to rush Pacman, or flee when scared."
    def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
        self.index = index
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scaredFlee

    def getDistribution( self, state ):
        # Read variables from state
        ghostState = state.getGhostState( self.index )
        legalActions = state.getLegalActions( self.index )
        pos = state.getGhostPosition( self.index )
        isScared = ghostState.scaredTimer > 0

        speed = 1
        if isScared: speed = 0.5

        actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
        newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
        pacmanPosition = state.getPacmanPosition()

        # Select best actions given the state
        distancesToPacman = [state.dist[( pos, pacmanPosition )] for pos in newPositions]

        if isScared:
            bestScore = max( distancesToPacman )
            bestProb = self.prob_scaredFlee
        else:
            bestScore = min( distancesToPacman )
            bestProb = self.prob_attack
        bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]

        # Construct distribution
        dist = util.Counter()
        for a in bestActions: dist[a] = bestProb / len(bestActions)
        for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
        dist.normalize()
        return dist
