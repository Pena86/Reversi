import time

class Human:
    """Class for human players
    """
    def __init__(self, callBack):
        self.move = (-1,-1)
        self.run = False
        self.checkKeyPressed = callBack
        self.player = -1

    def gameStart(self, playerNo):
        """Method to call when game round starts
        """
        self.run = True
        self.player = playerNo
    
    def makeMove(self, turn, board, makeMoveCallBack):
        """Method o call when it's time to make a move
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

