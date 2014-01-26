import time, random

class Game_ai:
    """Example Ai class
    """
    def __init__(self):
        self.move = (-1,-1)
        self.run = False
        self.board = []
        self.player = -1

    def gameStart(self, playerNo):
        """Method to call when game round starts
        """
        self.run = True
        self.player = playerNo
    
    def makeMove(self, turnNo, boardSituation, validMoves, makeMoveCallBack):
        """Method to call when it's time to make a move
        """
        time.sleep(0.1)
        self.board = boardSituation

        if len(validMoves):
            makeMoveCallBack(validMoves[random.randrange(len(validMoves))])
        else:
            print ("Randomizer: No valid moves")

    def gameEnd(self):
        """Method to call when game roun ends
        """
        self.run = False
