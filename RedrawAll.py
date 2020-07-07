
#This file is mainly responsible for drawing out the sidebars and the grids that are shown in the game. 

from Classes import *
####################################
#RedrawAll
####################################
#This draws the board
def drawBoard(canvas, data):
    for row in range(data.rows - 1):
        for col in range(data.cols - 1):
            canvas.create_rectangle(col * data.cellWidth + data.margin, 
                                    row * data.cellHeight + data.margin, 
                                    (col + 1) * data.cellWidth + data.margin, 
                                    (row + 1) * data.cellHeight + data.margin,
                                    fill = '#EBCD7D', width = 4)

#Draws all pieces on the board
def drawPieces(canvas, data):
    for row in range(data.rows):
        for col in range(data.cols):
            piece = data.board[row][col]
            if isinstance(piece, Piece):
                piece.draw(canvas, data)

#Draws the game over state of the game
def gameOver(canvas, data):
    if data.gameOver:
        canvas.create_rectangle(data.width / 2 - 140, data.height / 2 - 40, \
                                data.width / 2 + 140, data.height / 2 + 40, \
                                fill = 'white')
        canvas.create_text(data.width / 2, data.height / 2, text = '%s Won!'%(data.winner), \
                           font="Times 50 bold italic", fill = '#545454')

             ####################################
             #SideBar
             ####################################
def drawCurrentMove(canvas, data, x0, y0, x1, y1, margin, rowNum):
    x2, y2, x3, y3 = (x0 + margin, y0 + margin * (rowNum + 1) + rowNum * data.cellHeight,\
                            x1 - margin, y0 + margin * (rowNum + 1) + (rowNum + 1)*data.cellHeight)
    canvas.create_rectangle(x2, y2, x3, y3)
    if data.playerTurn:
        currentPlayer = 'White'
    else:
        currentPlayer = 'Black'
    canvas.create_text((x2 + x3)/2, (y2 + y3)/2, text = 'Making the Move : %s' % currentPlayer)

def drawTimer(canvas, data, x0, y0, x1, y1, margin, rowNum):
    x2, y2, x3, y3 = (x0 + margin, y0 + margin * (rowNum + 1) + rowNum * data.cellHeight,\
                            x1 - margin, y0 + margin * (rowNum + 1) + (rowNum + 1)*data.cellHeight)
    canvas.create_rectangle(x2, y2, x3, y3)
    canvas.create_text((x2 + x3)/2, (y2 + y3)/2, text = 'Time Left : %d' %(data.timer))

def drawRedo(canvas, data, x0, y0, x1, y1, margin, rowNum):
    x2, y2, x3, y3 = (x0 + margin, y0 + margin * (rowNum + 1) + rowNum * data.cellHeight,\
                            x1 - margin, y0 + margin * (rowNum + 1) + (rowNum + 1)*data.cellHeight)
    canvas.create_rectangle(x2, y2, x3, y3)
    canvas.create_text((x2 + x3)/2, (y2 + y3)/2, text = 'Undo Move')

def drawScore(canvas, data, x0, y0, x1, y1, margin, rowNum):
    x2, y2, x3, y3 = (x0 + margin, y0 + margin * (rowNum + 1) + rowNum * data.cellHeight,\
                            x1 - margin, y0 + margin * (rowNum + 1) + (rowNum + 1)*data.cellHeight)
    canvas.create_rectangle(x2, y2, x3, y3)
    canvas.create_text((x2 + x3)/2, (y2 + y3)/2, text = 'White = %d   Black = %d' %(data.scores['White'], data.scores['Black']))

def drawMode(canvas, data, x0, y0, x1, y1, margin, rowNum):
    x2, y2, x3, y3 = (x0 + margin, y0 + margin * (rowNum + 1) + rowNum * data.cellHeight,\
                            x1 - margin, y0 + margin * (rowNum + 1) + (rowNum + 1)*data.cellHeight)
    canvas.create_rectangle(x2, y2, x3, y3)
    if data.gameMode == 'Multiplayer':
        canvas.create_text((x2 + x3)/2, (y2 + y3)/2, text = 'Mode : %s'%data.gameMode)
    elif data.gameMode == 'AI':
        canvas.create_text((x2 + x3)/2 - 30, (y2 + y3)/2, text = 'Mode : %s  [Difficulty : %d]'%(data.gameMode, data.hardLevel))
        canvas.create_rectangle((x2 + x3)/2 + 60, y2 + 5, (x2 + x3)/2 + 90, (y2 + y3)/2 - 2)
        canvas.create_rectangle((x2 + x3)/2 + 60, (y2 + y3)/2 + 2, (x2 + x3)/2 + 90, y3 - 5)
        canvas.create_polygon((x2 + x3)/2 + 75, y2 + 10, (x2 + x3)/2 + 70, (y2 + y3)/2 - 8, (x2 + x3)/2 + 80, (y2 + y3)/2 - 8)
        canvas.create_polygon((x2 + x3)/2 + 75, y3 - 10, (x2 + x3)/2 + 70, (y2 + y3)/2 + 8, (x2 + x3)/2 + 80, (y2 + y3)/2 + 8)

def drawInstructions(canvas, data, x0, y0, x1, y1, margin, rowNum):
    x2, y2, x3, y3 = (x0 + margin, y0 + margin * (rowNum + 1) + rowNum * data.cellHeight,\
                            x1 - margin, y1 - margin)
    canvas.create_rectangle(x2, y2, x3, y3)
    cx, cy = ((x2 + x3)/2, (y2 + y3)/2)
    canvas.create_text(cx, cy - 3 * data.cellHeight, text = 'How to play this game :')
    canvas.create_text(cx, cy - 2 * data.cellHeight, text = 'Connect 5 to win!')
    canvas.create_text(cx, cy - data.cellHeight, text = 'Click on \'Mode\' button to toggle between')
    canvas.create_text(cx, cy - data.cellHeight + 15, text = 'AI and Multuplayer')
    canvas.create_text(cx, cy, text = 'Press \'r\' to reset game')
    canvas.create_text(cx, cy + data.cellHeight, text = 'Press \'c\' to play another match')
    canvas.create_text(cx, cy + 2 * data.cellHeight, text = 'Press Undo to undo a move!')
    
    
def drawInstructionMultiplayer(canvas, data, x0, y0, x1, y1, margin, rowNum):
    x2, y2, x3, y3 = (x0 + margin, y0 + margin * (rowNum + 1) + rowNum * data.cellHeight,\
                            x1 - margin, y1 - margin)
    canvas.create_rectangle(x2, y2, x3, y3)
    cx, cy = ((x2 + x3)/2, (y2 + y3)/2)
    canvas.create_text(cx, cy - 2 * data.cellHeight, text = 'How to play this game :')
    canvas.create_text(cx, cy - data.cellHeight, text = 'Connect 5 to win!')
    canvas.create_text(cx, cy, text = 'Press \'c\' to continue after a match!')
    canvas.create_text(cx, cy + 15, text = '(Needs Confirmation)')
    canvas.create_text(cx, cy + data.cellHeight, text = 'Keep a watch out for time!')
    canvas.create_text(cx, cy + data.cellHeight + 15, text = 'You will skip your turn if the time is up!')
def drawSideBar(canvas, data):
#Current Move player
#Timer
#Redo
#Score for both players
    x0 = (data.cols - 1) * data.cellWidth + 2 * data.margin
    y0 = data.margin
    x1 = data.width - data.margin
    y1 = data.height - data.margin
    margin = 10
    canvas.create_rectangle(x0, y0, x1, y1)
    drawCurrentMove(canvas, data, x0, y0, x1, y1, margin, 0)
    drawTimer(canvas, data, x0, y0, x1, y1, margin, 1)
    drawRedo(canvas, data, x0, y0, x1, y1, margin, 2)
    drawScore(canvas, data, x0, y0, x1, y1, margin, 3)
    drawMode(canvas, data, x0, y0, x1, y1, margin, 4)
    drawInstructions(canvas, data, x0, y0, x1, y1, margin, 5)
    
def drawSideBarMultiplayer(canvas, data):
    x0 = (data.cols - 1) * data.cellWidth + 2 * data.margin
    y0 = data.margin
    x1 = data.width - data.margin
    y1 = data.height - data.margin
    margin = 10
    canvas.create_rectangle(x0, y0, x1, y1)
    drawCurrentMove(canvas, data, x0, y0, x1, y1, margin, 0)
    drawTimer(canvas, data, x0, y0, x1, y1, margin, 1)
    drawScore(canvas, data, x0, y0, x1, y1, margin, 2)
    drawInstructionMultiplayer(canvas, data, x0, y0, x1, y1, margin, 3)
    
def drawWelcomePage(canvas, data):
    width = 400
    height = 100
    x0, y0, x1, y1 = data.width / 2 - width, data.height / 2 - height, data.width / 2 + width, data.height / 2 + height
    
    canvas.create_rectangle(x0, y0, x1, y1, fill = '#EBCD7D')
    canvas.create_text(data.width / 2, data.height / 2 - 50, text = 'Welcome to Gomoku!', fill = 'black', font = 'Helvetica 60 bold italic')
    canvas.create_text(data.width / 2, data.height / 2 + 50, text = 'Press any key to start', fill = 'black')
    
    
    
    
    
    