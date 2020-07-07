
#This file is responsible setting up the single-window version of the game

from tkinter import *
from MousePressed import *
from RedrawAll import *
from ArticifialIntelligence import *
####################################
# Animation Functions
####################################

def init(data): 
    data.chessWidth = 900
    data.chessHeight = 900
    data.rows = 15  #Must take into account last row
    data.cols = 15 
    data.margin = 50
    data.cellWidth = (data.chessWidth - (2 * data.margin)) / (data.cols - 1)
    data.cellHeight = (data.chessHeight - (2 * data.margin)) / (data.rows - 1)
    data.board = [[0] * data.cols for row in range(data.rows)]
    data.playerTurn = False
    data.dir = [[(-1, -1), (1, 1)], [(0, -1), (0, 1)], [(1, -1), (-1, 1)], [(-1, 0), (1, 0)]]
    data.gameOver = False
    data.winner = None
    data.timer = 60
    data.timerDelay = 1000
    data.pieceOrder = [] #This is to record the order to place the pieces
    data.scores = {'White':0, 'Black':0}
    data.surroundSet = set() #This holds the surrounding pieces
    data.gameMode = 'Multiplayer' 
    data.welcomePage = True
    data.hardLevel = 3
    data.prevPlaced = None
    data.ThisIsWierd = "What the hell is this, I am actually kind of scared"
    pass


def mousePressed(event, data):
    # use event.x and event.y
#The booleans are to make sure that when an individual overclicks, that no error occurs
    if data.gameMode == 'AI':
        makingMove = False
        rowNum, colNum, rowPos, colPos = isValid(data, event.x, event.y)
        playerNotMoved = rowNum == -1 or colNum == -1 or data.board[rowPos][colPos] != 0
        if not data.gameOver:
            if not data.playerTurn and not playerNotMoved:
                makeMove(data, event.x, event.y)#Human turn
                makingMove = True
#First checks if player has won
            if not data.gameOver and makingMove:
#Machine automatically makes the next move
                getBestBoardScore(data, [], data.hardLevel)
            clickedUp = isArrowBarClickedUp(data, event.x, event.y)
            clickedDown = isArrowBarClickedDown(data, event.x, event.y)
            if clickedUp:
                if 0 <= data.hardLevel + 1 <= 3:
                    data.hardLevel += 1
            if clickedDown:
                if 0 <= data.hardLevel - 1 <= 3:
                    data.hardLevel -= 1
            undoMove(data, event.x, event.y)
            undoMove(data, event.x, event.y)
            if not clickedUp and not clickedDown:
                modeClicked(data, event.x, event.y)
    elif data.gameMode == 'Multiplayer':
        if not data.gameOver and data.welcomePage == False:
            makeMove(data, event.x, event.y)
            undoMove(data, event.x, event.y)
            modeClicked(data, event.x, event.y)
    pass


#This function is to check is the user has clicked on the game mode to change it
#This should be in Mouse Pressed but I cannot perform circular import
def modeClicked(data, x, y):
    if isSideBarClicked(data, x, y, 4):
        currentMode = data.gameMode
        data.chessWidth = 900
        data.chessHeight = 900
        data.rows = 15  #Must take into account last row
        data.cols = 15 
        data.margin = 50
        data.cellWidth = (data.chessWidth - (2 * data.margin)) / (data.cols - 1)
        data.cellHeight = (data.chessHeight - (2 * data.margin)) / (data.rows - 1)
        data.board = [[0] * data.cols for row in range(data.rows)]
        data.playerTurn = False
        data.dir = [[(-1, -1), (1, 1)], [(0, -1), (0, 1)], [(1, -1), (-1, 1)], [(-1, 0), (1, 0)]]
        data.gameOver = False
        data.winner = None
        data.timer = 60
        data.timerDelay = 1000
        data.pieceOrder = [] #This is to record the order to place the pieces
        data.scores = {'White':0, 'Black':0}
        data.surroundSet = set() #This holds the surrounding pieces
        data.welcomePage = False
        data.hardLevel = 3
        data.prevPlaced = None
        if currentMode == 'AI':
            data.gameMode = 'Multiplayer'
        elif currentMode == 'Multiplayer':
            data.gameMode = 'AI'

def keyPressed(event, data):
    # use event.char and event.keysym
    if data.welcomePage == True:
        data.welcomePage = False
    else:
        if event.char == 'r': #Redo the game..
            data.chessWidth = 900
            data.chessHeight = 900
            data.rows = 15  #Must take into account last row
            data.cols = 15 
            data.margin = 50
            data.cellWidth = (data.chessWidth - (2 * data.margin)) / (data.cols - 1)
            data.cellHeight = (data.chessHeight - (2 * data.margin)) / (data.rows - 1)
            data.board = [[0] * data.cols for row in range(data.rows)]
            data.playerTurn = False
            data.dir = [[(-1, -1), (1, 1)], [(0, -1), (0, 1)], [(1, -1), (-1, 1)], [(-1, 0), (1, 0)]]
            data.gameOver = False
            data.winner = None
            data.timer = 60
            data.timerDelay = 1000
            data.pieceOrder = [] #This is to record the order to place the pieces
            data.scores = {'White':0, 'Black':0}
            data.surroundSet = set() #This holds the surrounding pieces
            data.gameMode = 'Multiplayer'
            data.welcomePage = False
            data.prevPlaced = None
        elif event.char == 'c' and data.gameOver: #Continue playing the game
            scoreDict = data.scores
            currentMode = data.gameMode
            data.chessWidth = 900
            data.chessHeight = 900
            data.rows = 15  #Must take into account last row
            data.cols = 15 
            data.margin = 50
            data.cellWidth = (data.chessWidth - (2 * data.margin)) / (data.cols - 1)
            data.cellHeight = (data.chessHeight - (2 * data.margin)) / (data.rows - 1)
            data.board = [[0] * data.cols for row in range(data.rows)]
            data.playerTurn = False
            data.dir = [[(-1, -1), (1, 1)], [(0, -1), (0, 1)], [(1, -1), (-1, 1)], [(-1, 0), (1, 0)]]
            data.gameOver = False
            data.winner = None
            data.timer = 60
            data.timerDelay = 1000
            data.pieceOrder = [] #This is to record the order to place the pieces
            data.scores = scoreDict
            data.surroundSet = set() #This holds the surrounding pieces
            data.gameMode = currentMode
            data.welcomePage = False
            data.prevPlaced = None
    pass

def timerFired(data):
    if not data.gameOver and not data.welcomePage:
        data.timer -= 1
    if data.timer == 0:
        switchPlayer(data)
        if data.gameMode == 'AI':
            if len(data.surroundSet) == 0:
                addPiece(data, 7, 7, True)
            else:
                getBestBoardScore(data, [], data.hardLevel)
    pass

def redrawAll(canvas, data):
    if data.welcomePage == True:
        drawWelcomePage(canvas, data)
    else:
        canvas.create_rectangle(0, 0, data.width, data.height, fill = 'white')
        drawBoard(canvas, data)
        drawPieces(canvas, data)
        gameOver(canvas, data)
        drawSideBar(canvas, data)
    pass

#Check CitedCode for citations
    
def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1300, 900)