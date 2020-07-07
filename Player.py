
#This file is mainly reponsible for displaying what each screen will display for the multiple-screen
#version of the game and how each computer sends and recieves info from the server. 

#Check CitedCode for specific citations

import socket
import threading
from queue import Queue
from MousePressed import *
from RedrawAll import *
from ArticifialIntelligence import *
from tkinter import *


IP = input('Please Type The IP Here\n')
HOST = IP # put your IP address here if playing on multiple computers
PORT = 50003

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST,PORT))
print("connected to server")

def handleServerMsg(server, serverMsg):
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n") #Splits the incoming messages into different messges
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:]) #Takes out of the first message
      serverMsg.put(readyMsg)
      command = msg.split("\n")

# events-example0.py from 15-112 website
# Barebones timer, mouse, and keyboard events

####################################
# customize these functions
####################################

def init(data):
    data.movingPlayer = 'playerOne'
    data.myID = None
    data.opponentID = None
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
    data.status = False
    data.statusPrint = 'Player One Ready : False   Player Two Ready : False'
    data.cont = None
    data.contPrint = 'Player One Continue : False   Player Two Continue : False'
    data.prevPlaced = None

def mousePressed(event, data):
    if data.status == True:
        msg = ''
        if not data.gameOver:
            if data.movingPlayer == data.myID and makeMove(data, event.x, event.y):
                msg = 'makeMove %d %d\n' % (event.x, event.y)
                data.movingPlayer = data.opponentID
                data.timer = 60
        if (msg != ""):
            print ("sending: ", msg,)
            data.server.send(msg.encode())
        
        
def keyPressed(event, data):
    if data.status == False:
        msg = 'status True\n'
        data.server.send(msg.encode())
        print('Status Message Sent!')
    else:
        if event.char == 'c' and data.gameOver == True:
            msg = 'continue True\n'
            data.server.send(msg.encode())
            print('continue request sent!')
        elif event.char == 'y' and data.cont == False:
            msg = 'continue True\n'
            data.server.send(msg.encode())
            print('continue request sent!')
        elif event.char == 'n' and data.cont == False:
            msg = 'continue close\n'
            data.server.send(msg.encode())
    pass


def timerFired(data):
    # timerFired receives instructions and executes them
    if not data.gameOver:
        data.timer -= 1
    if data.timer == 0:
        if data.movingPlayer == data.myID:
            data.movingPlayer = data.opponentID
        elif data.movingPlayer == data.opponentID:
            data.movingPlayer = data.myID
        data.playerTurn = not data.playerTurn
        data.timer = 60
    while (serverMsg.qsize() > 0):
        msg = serverMsg.get(False) #Gets a message from the message queue
        print("received: ", msg, "\n")
        msg = msg.split()
        command = msg[0] #Finds the command and executes the message
        if (command == 'status'):
            if msg[5] == 'True':
                firstBool = True
            else:
                firstBool = False
            if msg[10] == 'True':
                secondBool = True
            else:
                secondBool = False
            data.status = firstBool and secondBool
            data.statusPrint = ' '.join(msg[1:])
            if data.status:
                data.timer = 60
        elif (command == 'continue'):
            if msg[10] == 'close' or msg[5] == 'close':
                data.cont = None
                continue
            if msg[5] == 'True':
                firstBool = True
            else:
                firstBool = False
            if msg[10] == 'True':
                secondBool = True
            else:
                secondBool = False
            data.cont = firstBool and secondBool
            data.contPrint = ' '.join(msg[1:])
            if data.cont == True:
                data.movingPlayer = 'playerOne'
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
                data.hardLevel = 3
                data.cont = None
                data.contPrint = 'Player One Continue : False   Player Two Continue : False'
                data.prevPlaced = None
        elif (command == "myIDis"):
            data.myID = msg[1]

        elif (command == "newPlayer"):
            data.opponentID = msg[1]

        elif (command == "makeMove"):
            print('hello')
            x = int(msg[2])
            y = int(msg[3])
            makeMove(data, x, y)
            data.movingPlayer = data.myID
            data.timer = 60
      
        
def drawMovingPlayer(canvas, data, rowNum):
    x0 = (data.cols - 1) * data.cellWidth + 2 * data.margin
    y0 = data.margin
    x1 = data.width - data.margin
    y1 = data.height - data.margin
    margin = 10
    x2, y2, x3, y3 = (x0 + margin, y0 + margin * (rowNum + 1) + rowNum * data.cellHeight,\
                            x1 - margin, y0 + margin * (rowNum + 1) + (rowNum + 1)*data.cellHeight)
    if data.movingPlayer == data.myID:
        canvasText = '(Your turn!)'
    else:
        canvasText = '(Opponent turn!)'
    canvas.create_text((x2 + x3)/2, (y2 + y3)/2 + 15, text = canvasText, font="Times 10 bold italic" )
      


    data.statusPrint = 'Player One Ready : False   Player Two Ready : False'
    data.cont = None
    data.contPrint = 'Player One Continue : False   Player Two Continue : False'

def redrawAll(canvas, data):
    if data.status == False:
        listStatusPrint = data.statusPrint.split(' ')
        canvas.create_rectangle(0, 0, data.width, data.height , fill = '#EBCD7D')
        canvas.create_text(data.width / 2, data.height / 2 - 45, text = ' '.join(listStatusPrint[:5]), font="Times 50 bold italic")
        canvas.create_text(data.width / 2, data.height / 2 + 5, text = ' '.join(listStatusPrint[5:]), font="Times 50 bold italic")
        canvas.create_text(data.width / 2 , data.height / 2 + 55, text = 'Press any key to get ready!', font="Times 50 bold italic")
        canvas.create_text(data.width / 2, data.height / 2 + 105, text = '(You are %s !)'%data.myID, font = "Times 20 bold italic")
    elif data.cont == False:
        listContPrint = data.contPrint.split(' ')
        canvas.create_rectangle(0, 0, data.width, data.height , fill = '#EBCD7D')
        canvas.create_text(data.width / 2, data.height / 2 - 25, text = ' '.join(listContPrint[:5]), font="Times 50 bold italic")
        canvas.create_text(data.width / 2, data.height / 2 + 25, text = ' '.join(listContPrint[5:]), font="Times 50 bold italic")
        canvas.create_text(data.width / 2 , data.height / 2 + 75, text = 'y/n to continue to next match', font="Times 50 bold italic")
        canvas.create_text(data.width / 2, data.height / 2 + 105, text = '(You are %s !)'%data.myID, font = "Times 20 bold italic")
    else:
        canvas.create_rectangle(0, 0, data.width, data.height, fill = 'white')
        drawBoard(canvas, data)
        drawPieces(canvas, data)
        gameOver(canvas, data)
        drawSideBarMultiplayer(canvas, data)
        drawMovingPlayer(canvas, data, 0)


####################################
# use the run function as-is
####################################

#The following code was taken from the 15112 website
def run(width, height, serverMsg=None, server=None):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
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
    data.server = server
    data.serverMsg = serverMsg
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
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


serverMsg = Queue(100) #This creates a unique queue recieved from server
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

run(1300, 900, serverMsg, server)
