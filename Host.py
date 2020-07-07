
#This function is mainly responsible for setting up the host server for the multipl-screen version of the game

#Check CitedCode for specific citations

import socket
import threading
from queue import Queue

IP = socket.gethostbyname(socket.gethostname())
HOST = str(IP) # put your IP address here if playing on multiple computers
PORT = 50003
BACKLOG = 4

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
print("This is the IP : %s"%(IP))
print("looking for connection")

def handleClient(client, serverChannel, cID, clientele):
  client.setblocking(1)
  msg = ""
  while True:
    try:
      msg += client.recv(10).decode("UTF-8") #Recieves the messages, decode it, and splits on \n
      command = msg.split("\n")
      while (len(command) > 1):
        readyMsg = command[0]
        msg = "\n".join(command[1:])#Takes first message of all the messages
        serverChannel.put(str(cID) + " " + readyMsg) #Puts it on the server channel and tells everyone it was you who sent it
        command = msg.split("\n") #This will be put into the serverthread and distributed
    except:
      # we failed
      return

def serverThread(clientele, serverChannel):
  while True:
    msg = serverChannel.get(True, None) #Gets a message from the server channel (messages added by handleClient)
    print("msg recv: ", msg)
    msgList = msg.split(" ")
    senderID = msgList[0] #Gets the senderID (added in handleClient)
    instruction = msgList[1] #Instructions
    if instruction == 'status':
        print('status update recieved')
        global playerStatus
        playerStatus[senderID] = msgList[2]
        sendMsg = 'status Player One Ready : ' +  playerStatus['playerOne'] + '  Player Two Ready : ' + playerStatus['playerTwo'] + '\n'
        for cID in clientele:
            clientele[cID].send(sendMsg.encode())
        serverChannel.task_done()
        continue
    if instruction == 'continue':
        print('Continue request recieved!')
        global requestStatus
        print(requestStatus)
        requestStatus[senderID] = msgList[2]
        sendMsg = 'continue Player One Continue : ' +  requestStatus['playerOne'] + '  Player Two Continue : ' + requestStatus['playerTwo'] + '\n'
        for cID in clientele:
            clientele[cID].send(sendMsg.encode())
        if requestStatus['playerOne'] == 'True' and requestStatus['playerTwo'] == 'True':
            requestStatus['playerOne'] = 'False'
            requestStatus['playerTwo'] = 'False' #Setting the request status back to original
        if requestStatus['playerOne'] == 'close' or requestStatus['playerTwo'] == 'close':
            requestStatus['playerOne'] = 'False'
            requestStatus['playerTwo'] = 'False' #Setting the request status back to original
        serverChannel.task_done()
        continue
    details = " ".join(msgList[2:])
    if (details != ""):
      for cID in clientele:
        if cID != senderID:
          sendMsg = instruction + " " + senderID + " " + details + "\n" #Sends it to all other members
          clientele[cID].send(sendMsg.encode())
          print("> sent to %s:" % cID, sendMsg[:-1])
    print()
    serverChannel.task_done()


requestStatus = {'playerOne':'False', 'playerTwo':'False'} #Continuing or not
playerStatus = {'playerOne':'False', 'playerTwo':'False'} #Starting or not
clientele = dict()
playerNum = 0 #Looking for new player to join

serverChannel = Queue(100)
threading.Thread(target = serverThread, args = (clientele, serverChannel)).start()

names = ['playerOne', 'playerTwo']

while True:
  client, address = server.accept()
  # myID is the key to the client in the clientele dictionary
  myID = names[playerNum] #Gives new player a name
  print(myID, playerNum)
  for cID in clientele:
    print (repr(cID), repr(playerNum))
    clientele[cID].send(("newPlayer %s\n" % myID).encode()) #Informs other player that new player has joined
    client.send(("newPlayer %s\n" % cID).encode()) #Sends existing players to new player
  clientele[myID] = client #Adds new client into clientele
  client.send(("myIDis %s \n" % myID).encode()) #Sends client his own name
  print("connection recieved from %s" % myID)
  threading.Thread(target = handleClient, args = 
                        (client ,serverChannel, myID, clientele)).start()
  playerNum += 1
