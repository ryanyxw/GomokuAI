
#This function is mainly reponsible for, given a piece position, calculate the points that making the move would give

from Classes import *

#This function compairs two positions to see if they are the same type
def sameType(data, rowOne, colOne, rowTwo, colTwo):
    pieceOne = data.board[rowOne][colOne]
    pieceTwo = data.board[rowTwo][colTwo]
    if type(pieceOne) == WhitePiece or type(pieceOne) == WhitePieceNew:
        if type(pieceTwo) == WhitePiece or type(pieceTwo) == WhitePieceNew:
            return True
    elif type(pieceOne) == BlackPiece or type(pieceOne) == BlackPieceNew:
        if type(pieceTwo) == BlackPiece or type(pieceTwo) == BlackPieceNew:
            return True
    return False


#This goes in one direction and records number of consecutive pieces and their ends
def tryDirectionFind(data, rowNum, colNum, direction, consecutive, endCount):
#Checking both directions and counting together
    nextRow = rowNum + direction[0]
    nextCol = colNum + direction[1]
#First checks if it is out of bounds
    if 0 <= nextRow <= data.rows - 1 and 0 <= nextCol <= data.cols - 1:
        if data.board[nextRow][nextCol] == 0:
            return (consecutive, endCount)
        if not sameType(data, rowNum, colNum, nextRow, nextCol):
#Records that there is a block on one end
            endCount += 1
            return (consecutive, endCount)
        else:
            return tryDirectionFind(data, nextRow, nextCol, direction, consecutive + 1, endCount)
    else:
        return (consecutive, endCount)
    
#For a given point, this function checks how many types can be gotten with the single point
def getTypes(data, rowNum, colNum):
    connectType = {'five':0, 'openFour':0, 'closedFour':0, 'openThree':0, 'closedThree':0,\
                   'openTwo':0, 'closedTwo':0}
    for direction in data.dir:
        directionOne = direction[0]
        directionTwo = direction[1]
        solutionOne, endOne = tryDirectionFind(data, rowNum, colNum, directionOne, 0, 0)
        solutionTwo, endTwo = tryDirectionFind(data, rowNum, colNum, directionTwo, 0, 0)
#Maximum connected pieces
        maxConnect = solutionOne + solutionTwo + 1
        endBehavior = endOne + endTwo
        if maxConnect == 5:
            connectType['five'] += 1
        else:
            if maxConnect == 4 and endBehavior == 0:
                connectType['openFour'] += 1
            if maxConnect == 4 and endBehavior == 1:
                connectType['closedFour'] += 1
            if maxConnect == 3 and endBehavior == 0:
                connectType['openThree'] += 1
            if maxConnect == 3 and endBehavior == 1:
                connectType['closedThree'] += 1
            if maxConnect == 2 and endBehavior == 0:
                connectType['openTwo'] += 1
            if maxConnect == 2 and endBehavior == 1:
                connectType['closedTwo'] += 1
    return connectType


def getScore(data, rowNum, colNum, isSelf, scoreList, maxDepth):
    finalScore = 0
    connectType = getTypes(data, rowNum, colNum)
    multiplier = maxDepth - len(scoreList) #The more front the move will execute, the more points it will be worth
    if connectType['five'] != 0:
            finalScore = 1000000 * multiplier
    if isSelf:
        finalScore += (openFour(connectType, 0)) * multiplier
        finalScore += (doubleClosedFour(connectType, 0)) * multiplier
        finalScore += (closedFourOpenThree(connectType, 0)) * multiplier
        finalScore += doubleOpenThree(connectType, 0) * multiplier
        finalScore += openThreeClosedThree(connectType, 0) * multiplier
        finalScore += singleClosedFour(connectType, 0) * multiplier
        finalScore += singleOpenThree(connectType, 0) * multiplier
        finalScore += doubleOpenTwo(connectType, 0) * multiplier
        finalScore += singleClosedThree(connectType, 0) * multiplier
        finalScore += singleOpenTwo(connectType, 0) * multiplier
        finalScore += singleClosedTwo(connectType, 0) * multiplier
        finalScore += 200
    else:
        finalScore += (openFour(connectType, 0)) * multiplier
        finalScore += (doubleClosedFour(connectType, 0)) * multiplier
        finalScore += (closedFourOpenThree(connectType, 0)) * multiplier
        finalScore += (doubleOpenThree(connectType, 0)) * multiplier
        finalScore += openThreeClosedThree(connectType, 0) * multiplier
        finalScore += singleClosedFour(connectType, 0) * multiplier
        finalScore += singleOpenThree(connectType, 0) * multiplier
        finalScore += doubleOpenTwo(connectType, 0) * multiplier
        finalScore += singleClosedThree(connectType, 0) * multiplier
        finalScore += singleOpenTwo(connectType, 0) * multiplier
        finalScore += singleClosedTwo(connectType, 0) * multiplier
    return finalScore

#The following functions are used in getScore
def openFour(connectType, score):
    return connectType['openFour'] * 200000
def doubleClosedFour(connectType, score):
    numPairs = connectType['closedFour']//2
    return numPairs * 200000
def closedFourOpenThree(connectType, score):
    numPairs = min(connectType['closedFour'], connectType['openThree'])
    return numPairs * 100000
def doubleOpenThree(connectType, score):
    numPairs = connectType['openThree']//2
    return numPairs * 10000
def openThreeClosedThree(connectType, score):
    numPairs = min(connectType['closedThree'], connectType['openThree'])
    return numPairs * 200
def singleClosedFour(connectType, score):
    return connectType['closedFour'] * 100
def singleOpenThree(connectType, score):
    return connectType['openThree'] * 1000
def doubleOpenTwo(connectType, score):
    numPairs = connectType['openTwo'] // 2
    return numPairs * 10
def singleClosedThree(connectType, score):
    return connectType['closedThree'] * 10
def singleOpenTwo(connectType, score):
    return connectType['openTwo'] * 5
def singleClosedTwo(connectType, score):
    return connectType['closedTwo'] * 3



        