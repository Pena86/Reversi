import timeit

"""
Just some speed testing with partial game setup
"""

class ReversiTuple:
    """Reversi game logig class
    """
    def __init__(self, movesCallBack = None, buttonsCheck = None):
        self.movesCallBack = movesCallBack
        self.buttonsCheck = buttonsCheck

        self.emptyTiles = 0
        self.whiteTiles = 0
        self.blackTiles = 0

        self.board = [[0 for x in range(8)] for x in range(8)]
        
        self.board[2][3] = 2
        self.board[2][4] = 1
        self.board[3][3] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        self.board[4][4] = 1
        self.board[5][3] = 1
        self.board[5][4] = 2

    def checkDirection(self, x, y, dx, dy, player, opponent):
        """Checks pieces to flip in the given direction and return a list of tuples for those pieces to flip.
            else return empty list
        """
        x += dx
        y += dy
        foundOpp = []
        while x < 8 and x > -1 and y < 8 and y > -1:
            #print (x, y, len(foundOpp))
            if self.board[x][y] == opponent:
                foundOpp.append((x,y))
                #print (foundOpp)
            elif len(foundOpp) > 0 and self.board[x][y] == player:
                #print ("found own")
                return foundOpp
            else:
                return []

            x += dx
            y += dy
        return []

    def checkIsValidMoves(self, player = 1):
        moves = []
        directionsToCheck = [(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]

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
                            moves.append((x,y))
                            #print ("found")
                            break

        return moves

class ReversiList:
    """Reversi game logig class
    """
    def __init__(self, movesCallBack = None, buttonsCheck = None):
        self.movesCallBack = movesCallBack
        self.buttonsCheck = buttonsCheck

        self.emptyTiles = 0
        self.whiteTiles = 0
        self.blackTiles = 0

        self.board = [[0 for x in range(8)] for x in range(8)]
        
        self.board[2][3] = 2
        self.board[2][4] = 1
        self.board[3][3] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        self.board[4][4] = 1
        self.board[5][3] = 1
        self.board[5][4] = 2

    def checkDirection(self, x, y, dx, dy, player, opponent):
        """Checks pieces to flip in the given direction and return a list of tuples for those pieces to flip.
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

    def checkIsValidMoves(self, player =1):
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


if __name__ == '__main__':
    a = ReversiTuple()
    b = ReversiList()
    print (timeit.repeat(a.checkIsValidMoves, repeat=3, number=1000))
    print (timeit.repeat(b.checkIsValidMoves, repeat=3, number=1000))