
class Reversi:
    """Reversi game logig class
    """
    def __init__(self, callBack):
        self.ui = callBack

    def setup(self):
        self.run = True
        self.winner = 0
        self.board = [[0 for x in range(8)] for x in range(8)]
        self.movesMade = []
        
        self.board[3][3] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        self.board[4][4] = 1

        self.turn = 1
        self.player = 1
        self.player1 = None
        self.player2 = None

    def roundStart(self, pl1, pl2):
        """Reversi game round start
        """
        self.player1 = pl1
        self.player2 = pl2

        self.player1.gameStart(1)
        self.player2.gameStart(2)

        while self.run:
            # ui check buttons
            # Player make move

            if self.player == 1:
                self.player1.makeMove(self.turn, self.board, self.moveTo)
                self.player = 2
            else:
                self.player2.makeMove(self.turn, self.board, self.moveTo)
                self.player = 1

            # ui draw board
            self.winner = self.checkGameEnd()
            if self.winner:
                self.run = False

    def moveTo(self, x, y):
        """Method for players to call when making a move in the game
        """
        if x != None and y != None and self.board[x][y] == 0 and self.validMove(x, y, self.player):
            self.movesMade.append([self.turn, self.player, [x,y]])
            self.turn += 1
            self.ui()
            return True
        return False

    def abort(self):
        """If the game needs to be aborted at the middle
        """
        self.run = False
        self.player1.gameEnd()
        self.player2.gameEnd()

    def validMove(self, x, y, player):
        """If the move is valid, it's made to the board and return True
            else return False
        """
        if player == 1:
            opponent = 2
        elif player == 2:
            opponent = 1
        else:
            print ("No player")
            return False
        #print (player, opponent, x, y)

        piecesToFlip = []
        directionsToCheck = [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]
        for direction in directionsToCheck:
            piecesToFlip.extend(self.checkDirection(x, y, direction[0], direction[1], player, opponent))
        #print (piecesToFlip)

        if len(piecesToFlip) > 0:
            self.board[x][y] = player
            for spot in piecesToFlip:
                self.board[spot[0]][spot[1]] = player
            return True
        return False

    def checkDirection(self, x, y, dx, dy, player, opponent):
        """Checks pieces to flip in the given ridection and return a list of tuples for those pieces to flip.
            else return empty list
        """
        x += dx
        y += dy
        foundOpp = []
        while x < 8 and x > -1 and y < 8 and y > -1:
            #print (x, y, len(foundOpp))
            if self.board[x][y] == opponent:
                foundOpp.append([x,y])
                #print (foundOpp)
            elif len(foundOpp) > 0 and self.board[x][y] == player:
                #print ("found own")
                return foundOpp
            else:
                return []

            x += dx
            y += dy
        return []

    def checkGameEnd(self):
        allTiles = [item for sublist in self.board for item in sublist]
        
        emptyTiles = sum(1 for tile in allTiles if tile == 0)
        whiteTiles = sum(1 for tile in allTiles if tile == 1)
        blackTiles = sum(1 for tile in allTiles if tile == 2)
        if not (emptyTiles and whiteTiles and blackTiles):
            if whiteTiles > blackTiles: #pl1 has won
                return 1
            elif whiteTiles < blackTiles: #pl2 has won
                return 2
            else:                           #draw
                return -1
        return False
