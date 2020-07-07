
#This file is main responsible for defining the different classes that are used in the game

def getDistance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5


class Piece(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.color = None
        self.radius = 20
    def draw(self, canvas, data):
        canvas.create_oval(self.col * data.cellWidth + data.margin - self.radius, 
                           self.row * data.cellHeight + data.margin - self.radius, 
                           self.col * data.cellWidth + data.margin + self.radius, 
                           self.row * data.cellHeight + data.margin + self.radius, 
                           fill = self.color)
        
class BlackPiece(Piece):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.color = 'black'

class WhitePiece(Piece):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.color = 'white'
        
        
class BlackPieceNew(BlackPiece):
    def __init__(self, row, col):
        super().__init__(row, col)
    def draw(self, canvas, data):
        canvas.create_oval(self.col * data.cellWidth + data.margin - self.radius, 
                           self.row * data.cellHeight + data.margin - self.radius, 
                           self.col * data.cellWidth + data.margin + self.radius, 
                           self.row * data.cellHeight + data.margin + self.radius, 
                           fill = self.color, outline = 'red')
       
class WhitePieceNew(WhitePiece):
    def __init__(self, row, col):
        super().__init__(row, col)
    def draw(self, canvas, data):
        canvas.create_oval(self.col * data.cellWidth + data.margin - self.radius, 
                           self.row * data.cellHeight + data.margin - self.radius, 
                           self.col * data.cellWidth + data.margin + self.radius, 
                           self.row * data.cellHeight + data.margin + self.radius, 
                           fill = self.color, outline = 'red')