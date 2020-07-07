
#This file is responsible for the AI calculations

import math
from Classes import *
from MousePressed import *
from Counting import *


####################################
# AI Makes Move
####################################
    
#This function gets the total number of connections a single piece has with its own type
def getMostConnections(data, rowNum, colNum):
    totalConnection = 0
    for direction in data.dir:
#5 in a row can go both ways
        directionOne = direction[0]
        directionTwo = direction[1]
        solutionOne = directionFind(data, rowNum, colNum, directionOne)
        solutionTwo = directionFind(data, rowNum, colNum, directionTwo)
        finalSolution = solutionOne + solutionTwo + 1
        totalConnection += finalSolution
    return totalConnection

def getMaxBoardScore(data, piece, maxDepth, depth, score, prevBestScore):
    count = 0
    if depth == maxDepth:
        return sum(score) 
    else:
        bestMove = None
        bestScore = float('-inf')
        for testPos in data.surroundSet:
            oldSurroundSet = data.surroundSet
            playerTurn = data.playerTurn #make sure player turn dosnt change 
            count += 1
            currentScore = 0
            rowPos, colPos = testPos
            addedElements1 = machineMove(data, rowPos, colPos)
#Changes the surrounding set accordingly
            isIn = (rowPos, colPos) in data.surroundSet
            if isIn:
                data.surroundSet.remove((rowPos, colPos))
            score.append(getScore(data, rowPos, colPos, True, score, maxDepth)) #True means self making the move
            currentScore = getMinBoardScore(data, testPos, maxDepth, depth + 1, score, bestScore)
            score.pop()
            if currentScore > bestScore:
                bestScore = currentScore
                bestMove = testPos
                if bestScore >= prevBestScore:
                    machineRecall(data, rowPos, colPos, addedElements1)
                    if isIn:
                        data.surroundSet.add((rowPos, colPos))
                    return bestScore
            machineRecall(data, rowPos, colPos, addedElements1)
            if isIn:
                data.surroundSet.add((rowPos, colPos))
            data.playerTurn = playerTurn #make sure player turn dosnt change during iterations
            assert(oldSurroundSet == data.surroundSet)
        return bestScore

def getMinBoardScore(data, piece, maxDepth, depth, score, prevBestScore):
    count = 0
    if depth == maxDepth:
        return sum(score)
    else:
        bestMove = None
        bestScore = math.inf
        for testPos in data.surroundSet:
            oldSurroundSet = data.surroundSet
            playerTurn = data.playerTurn #Make sure playerturn dosnt change
            count += 1
            currentScore = 0
            rowPos, colPos = testPos
            addedElements2 = machineMove(data, rowPos, colPos)
            isIn = (rowPos, colPos) in data.surroundSet
            if isIn:
                data.surroundSet.remove((rowPos, colPos))
                
            appendScore = getScore(data, rowPos, colPos, False, score, maxDepth)
            if appendScore >= 1000: # make sure that program always chooses to defend first
                appendScore += 200
            score.append(-1 * appendScore)
            currentScore = getMaxBoardScore(data, testPos, maxDepth, depth + 1, score, bestScore)
            score.pop()
            if currentScore < bestScore:
                bestScore = currentScore
                bestMove = testPos
                if bestScore <= prevBestScore:
                    machineRecall(data, rowPos, colPos, addedElements2)
                    if isIn:
                        data.surroundSet.add((rowPos, colPos))
                    return bestScore
            machineRecall(data, rowPos, colPos, addedElements2)
            if isIn:
                data.surroundSet.add((rowPos, colPos))
            data.playerTurn = playerTurn #make sure player turn dosnt change during iteration
            assert(oldSurroundSet == data.surroundSet)
        return bestScore

def getBestBoardScore(data, score, depth):
    bestMove = None
    bestScore = -math.inf
    for testPos in data.surroundSet:
        playerTurn = data.playerTurn #Make sure that playerturn does not change during iterations
        oldSurroundSet = data.surroundSet
        currentScore = 0
        rowPos, colPos = testPos
        addedElements3 = machineMove(data, rowPos, colPos)
        isIn = (rowPos, colPos) in data.surroundSet
        if isIn:
            data.surroundSet.remove((rowPos, colPos))
        score.append(getScore(data, rowPos, colPos, True, [], depth))
        currentScore = getMinBoardScore(data, testPos, depth, 0, score, bestScore)
        score.pop()
        if currentScore > bestScore:
            bestScore = currentScore
            bestMove = testPos
        machineRecall(data, rowPos, colPos, addedElements3)
        if isIn:
                data.surroundSet.add((rowPos, colPos))
        data.playerTurn = playerTurn #make sure dosnt change
        assert(oldSurroundSet == data.surroundSet)
    data.playerTurn = True
    addPiece(data, bestMove[0], bestMove[1], True)
