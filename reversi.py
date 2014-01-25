
class Reversi:
    """Reversi game logig class
    """
    def __init__(self, callBack):
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
        self.ui = callBack

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
            pass

    def moveTo(self, x, y):
        """Method for players to call when making a move in the game
        """
        if x != None and y != None:
            self.board[x][y] = self.player
            self.turn += 1
            self.ui()

        return True

    def abort(self):
        self.run = False
