import time

class Reversi:
    """Reversi game logig class
    """
    def __init__(self, movesCallBack, buttonsCheck):
        self.movesCallBack = movesCallBack
        self.buttonsCheck = buttonsCheck

        self.emptyTiles = 0
        self.whiteTiles = 0
        self.blackTiles = 0

    def roundStart(self, pl1, pl2):
        """Create a new game and start playing
        """
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

        self.player1 = pl1
        self.player2 = pl2

        self.player1.gameStart(1)
        self.player2.gameStart(2)

        self.movesCallBack()

        while self.run:
            #time.sleep(0.2)
            validMoves = self.checkIsValidMoves(self.player)

            if self.player == 1:
                self.player1.makeMove(self.turn, self.board, validMoves, self.moveTo)
                self.player = 2
                self.turn += 1
            else:
                self.player2.makeMove(self.turn, self.board, validMoves, self.moveTo)
                self.player = 1
                self.turn += 1

            self.winner = self.checkGameEnd()

            self.movesCallBack()
            if self.winner:
                self.run = False

            self.buttonsCheck()

        return [self.whiteTiles, self.blackTiles, 0, 0]

    def moveTo(self, x, y = None):
        """Method for players to call when making a move in the game
        """
        if type(x) == list:
            y = x[1]
            x = x[0]

        if x != None and y != None and self.board[x][y] == 0 and self.validMove(x, y, self.player):
            self.movesMade.append([self.turn, self.player, [x,y]])
            return True
            #TODO: if players have skipped turns, end game  :: self.turnSkipped = False
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
        """Checks if game has come to the end.
            TODO: if neither player can't make a turn, end game
        """
        allTiles = [item for sublist in self.board for item in sublist]
        
        self.emptyTiles = sum(1 for tile in allTiles if tile == 0)
        self.whiteTiles = sum(1 for tile in allTiles if tile == 1)
        self.blackTiles = sum(1 for tile in allTiles if tile == 2)
        if not (self.emptyTiles and self.whiteTiles and self.blackTiles):
            if self.whiteTiles > self.blackTiles: #pl1 has won
                return 1
            elif self.whiteTiles < self.blackTiles: #pl2 has won
                return 2
            else:                           #draw
                return -1
        return False

    def checkIsValidMoves(self, player):
        moves = []
        directionsToCheck = [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]

        if player == 1:
            opponent = 2
        elif player == 2:
            opponent = 1
        else:
            print ("No player")
            return moves

        for x in range(8):
            for y in range(8):
                if self.board[x][y] == 0:
                    for direction in directionsToCheck:
                        #print (x,y, directionsToCheck.index(direction))
                        if self.checkDirection(x, y, direction[0], direction[1], player, opponent) != []:
                            moves.append([x,y])
                            #print ("found")
                            break

        return moves
