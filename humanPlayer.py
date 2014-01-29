import time

class Game_ai:
    """Class for human players
    """
    def __init__(self, checkButtons):
        self.move = (-1,-1)
        self.run = False
        self.checkKeyPressed = checkButtons
        self.player = -1

    def gameStart(self, playerNo):
        """Method to call when game round starts
        """
        self.run = True
        self.player = playerNo
    
    def makeMove(self, turn, board, validMoves, makeMoveCallBack):
        """Method to call when it's time to make a move
        """
        turn = 1
        while turn and self.run:
            time.sleep(0.1)
            if self.checkKeyPressed():
                turn = 0
        pass

    def gameEnd(self):
        """Method to call when game roun ends
        """
        self.run = False

