
#This file is mainly responsible for performing everything that has to do with 
#the mousepressed, such as placing a piece on the grid or clicking on the sidebar


from Classes import *
####################################
#Mouse Pressed
####################################
#This helps locate the closest position of the closest intersection
def findClosestPosition(data, rowNum, colNum, x, y):
    corners = [(rowNum, colNum), (rowNum + 1, colNum), (rowNum, colNum + 1), (rowNum + 1, colNum + 1)]
    closestDis = 1000
    bestCorner = None
    for corner in corners:
        distance = getDistance(corner[0] * data.cellHeight + data.margin,\
                       corner[1] * data.cellWidth + data.margin, 
                       y, x)
        if  distance < closestDis:
            closestDis = distance
            bestCorner = corner
    return bestCorner

#This resets the timer and canges the current player
def switchPlayer(data):
    data.playerTurn = not data.playerTurn
    data.timer = 60

#This function first gets all the positions that are next to a given piece
def addSurrounding(data, row, col):
    if (row, col) in data.surroundSet:
        data.surroundSet.remove((row, col))
    for doubleDirection in data.dir:
        for singleDirection in doubleDirection:
            newRow = row + singleDirection[0]
            newCol = col + singleDirection[1]
            if 0 <= newRow < 15 and 0 <= newCol < 15 and \
            not isinstance(data.board[newRow][newCol], Piece): #Add that x and y cannot go out of bounds
                data.surroundSet.add((newRow, newCol))

#This creates a temporary addSurrouding variable that gives the machine the available spaces
def testAddSurrounding(data, row, col):
    addedElements = set()
    for doubleDirection in data.dir:
        for singleDirection in doubleDirection:
            newRow = row + singleDirection[0]
            newCol = col + singleDirection[1]
            if 0 <= newRow < 15 and 0 <= newCol < 15 and \
            not isinstance(data.board[newRow][newCol], Piece): #Add that x and y cannot go out of bounds
                addedElements.add((newRow, newCol))
    addedElements = addedElements.difference(data.surroundSet)
    data.surroundSet = data.surroundSet.union(addedElements)
    return addedElements


#This function adds a piece onto a board given its row and column
def addPiece(data, rowPos, colPos, isReal): #isReal checks if we actually want to add the piece onto the board or just trying
    if data.board[rowPos][colPos] != 0:
        return
    if not data.playerTurn:
        if not isReal:
            data.board[rowPos][colPos] = BlackPiece(rowPos, colPos)
#Checks if a 5 in the row has formed
        elif isReal:
            if data.prevPlaced != None:
                oldRowPos, oldColPos = data.prevPlaced
                if type(data.board[oldRowPos][oldColPos]) == BlackPieceNew:
                    data.board[oldRowPos][oldColPos] = BlackPiece(oldRowPos, oldColPos)
                elif type(data.board[oldRowPos][oldColPos]) == WhitePieceNew:
                    data.board[oldRowPos][oldColPos] = WhitePiece(oldRowPos, oldColPos)
            data.board[rowPos][colPos] = BlackPieceNew(rowPos, colPos)
            data.prevPlaced = (rowPos, colPos)
            data.pieceOrder.append((rowPos, colPos))
        if fiveInRow(data, rowPos, colPos) and isReal:
            data.gameOver = True
            data.winner = 'Black'
            data.scores['Black'] += 1
    elif data.playerTurn: #This is the AI turn
        if not isReal:
            data.board[rowPos][colPos] = WhitePiece(rowPos, colPos)
        elif isReal: #Only adds piece to order if it is real
            if data.prevPlaced != None:
                oldRowPos, oldColPos = data.prevPlaced
                if type(data.board[oldRowPos][oldColPos]) == BlackPieceNew:
                    data.board[oldRowPos][oldColPos] = BlackPiece(oldRowPos, oldColPos)
                elif type(data.board[oldRowPos][oldColPos]) == WhitePieceNew:
                    data.board[oldRowPos][oldColPos] = WhitePiece(oldRowPos, oldColPos)
            data.board[rowPos][colPos] = WhitePieceNew(rowPos, colPos)
            data.prevPlaced = (rowPos, colPos)
            data.pieceOrder.append((rowPos, colPos)) #Records the order
        if fiveInRow(data, rowPos, colPos) and isReal:
            data.gameOver = True
            data.winner = 'White'
            data.scores['White'] += 1
#This is to make sure that the machine is switching sides when it is calculating
    if not isReal:
        data.playerTurn = not data.playerTurn
        return testAddSurrounding(data, rowPos, colPos)
#Only adds to surrounding and switch players if the move is real
    else:
#Adds the new surroundings to the surrounding list
        addSurrounding(data, rowPos, colPos)
#Only changes the player when the move is finished
        switchPlayer(data)


#This function returns the closest position of the click as well as its top-left cell position
def isValid(data, x, y):
    relativeX = x - data.margin
    relativeY = y - data.margin
    rowNum, colNum = -1, -1
    for i in range(data.rows - 1):
        if i * data.cellWidth <= relativeX and (i+1) * data.cellWidth > relativeX:
            colNum = i
        if i * data.cellHeight <= relativeY and (i+1) * data.cellHeight > relativeY:
            rowNum = i
    if rowNum == -1 or colNum == -1:
        return (rowNum, colNum , None, None)
    rowPos, colPos = findClosestPosition(data, rowNum, colNum, x, y)
    return (rowNum, colNum, rowPos, colPos)
#This creates a new piece for real players
def makeMove(data, x, y):
    (rowNum, colNum, rowPos, colPos) = isValid(data, x, y)
    if rowNum == -1 or colNum == -1 or data.board[rowPos][colPos] != 0 or rowPos == None or colPos == None:
        print('Out of bounds')
        return False
    else:
        addPiece(data, rowPos, colPos, True)
        return True


#The following two functions are to try out all the options for the machine
#Machine Move makes the move (temporarily), and machine recall repeals the move
def machineMove(data, rowPos, colPos):
    #Finds the row and column
    return addPiece(data, rowPos, colPos, False)
def machineRecall(data, rowPos, colPos, addedElements):
    data.board[rowPos][colPos] = 0
#This resets the data.surroundingsets
    if addedElements != None:
        data.surroundSet = data.surroundSet.difference(addedElements)
#This is swapped because we have swapped the player turn within makeMove


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


#Checks if a 5 in a row has formed
#This checks if there is 5 in a row
def fiveInRow(data, rowNum, colNum):
    for direction in data.dir:
#5 in a row can go both ways
        directionOne = direction[0]
        directionTwo = direction[1]
        solutionOne = directionFind(data, rowNum, colNum, directionOne)
        solutionTwo = directionFind(data, rowNum, colNum, directionTwo)
        if solutionOne + solutionTwo + 1 >= 5:
            return True
    return False
        
def directionFind(data, rowNum, colNum, direction):
#Checking both directions and counting together
    nextRow = rowNum + direction[0]
    nextCol = colNum + direction[1]
#First checks if it is out of bounds
    if 0 <= nextRow <= data.rows - 1 and 0 <= nextCol <= data.cols - 1:
        if not sameType(data, rowNum, colNum, nextRow, nextCol):
            return 0
        else:
            return 1 + directionFind(data, nextRow, nextCol, direction)
    else:
        return 0

#This checks if the row in the sidebar is clicked
def isSideBarClicked(data, x, y, rowNum):
    x0 = (data.cols - 1) * data.cellWidth + 2 * data.margin
    y0 = data.margin
    x1 = data.width - data.margin
    y1 = data.height - data.margin
    margin = 10
    x2, y2, x3, y3 = (x0 + margin, y0 + margin * (rowNum + 1) + rowNum * data.cellHeight,\
                            x1 - margin, y0 + margin * (rowNum + 1) + (rowNum + 1)*data.cellHeight)
    return x2 <= x <= x3 and y2 <= y <= y3

def isArrowBarClickedUp(data, x, y):
    x0 = (data.cols - 1) * data.cellWidth + 2 * data.margin
    y0 = data.margin
    x1 = data.width - data.margin
    y1 = data.height - data.margin
    margin = 10
    rowNum = 4
    x2, y2, x3, y3 = (x0 + margin, y0 + margin * (rowNum + 1) + rowNum * data.cellHeight,\
                            x1 - margin, y0 + margin * (rowNum + 1) + (rowNum + 1)*data.cellHeight)
    x4, y4, x5, y5 = (x2 + x3)/2 + 60, y2 + 5, (x2 + x3)/2 + 90, (y2 + y3)/2 - 2
    return x4 <= x <= x5 and y4 <= y <= y5

def isArrowBarClickedDown(data, x, y):
    x0 = (data.cols - 1) * data.cellWidth + 2 * data.margin
    y0 = data.margin
    x1 = data.width - data.margin
    y1 = data.height - data.margin
    margin = 10
    rowNum = 4
    x2, y2, x3, y3 = (x0 + margin, y0 + margin * (rowNum + 1) + rowNum * data.cellHeight,\
                            x1 - margin, y0 + margin * (rowNum + 1) + (rowNum + 1)*data.cellHeight)
    x4, y4, x5, y5 = (x2 + x3)/2 + 60, (y2 + y3)/2 + 2, (x2 + x3)/2 + 90, y3 - 5
    return x4 <= x <= x5 and y4 <= y <= y5

def reCalcSurrounding(data):
    data.surroundSet = set()
    for row in range(data.rows - 1):
        for col in range(data.cols - 1):
            if data.board[row][col] != 0:
                addSurrounding(data, row, col)

#This function undoes the last move that the player has made
def undoMove(data, x, y):
    if isSideBarClicked(data, x, y, 2) and len(data.pieceOrder) != 0:
        lastMove = data.pieceOrder.pop()
        pieceType = data.board[lastMove[0]][lastMove[1]]
#You should first make sure that that if in AI mode, recalling moves should be done two at a time
        data.board[lastMove[0]][lastMove[1]] = 0
#Supposed to remove the coordinates from surrounding but should add it instead
        reCalcSurrounding(data)
        if type(pieceType) == WhitePiece or type(pieceType) == WhitePieceNew:
            data.playerTurn = True
            if len(data.pieceOrder) == 0:
                if data.gameMode == 'AI':
                    if len(data.surroundSet) == 0:
                        addPiece(data, 7, 7, True)
        elif type(pieceType) == BlackPiece or type(pieceType) == BlackPieceNew:
            data.playerTurn = False
        data.timer = 60
        
