import time, random

class Game_ai:
    """Example Ai class.
    This class contains all, what your AI class should also contain for competing at the possible unoffical tourmanent.

    The file name (whitout .py extension) is your AI's name at results.
    """
    def __init__(self, turnTime = 0, checkButtons = None):
        """Init of the class

        turnTime == int in secs to how long AI has time on each turn. 0 == infinite, but 'real' tournaments are planned to play either on 1 or 10 sec turns.
        checkButtons == function call to main.py's checkKeyPressed -function for the hummanPlayer.py. This might not be accessible on the final version of the game.
        """
        self.move = (-1,-1)
        self.run = False
        self.board = []
        self.player = -1
        self.turnTime = turnTime

    def gameStart(self, playerNo):
        """Method to call when game round starts.
        Init what you need before the round
        I'm planning to give this function it's own thread, but that's not ready yet

        playerNo == int [1|2] meaning your tokens on the board
        """
        self.run = True
        self.player = playerNo
    
    def makeMove(self, turnNo, boardSituation, validMoves, makeMoveCallBack):
        """Method to call when it's time to make a move.
        Within this function the AI should decide what move to make, and within the self.turnTime limit (game logic does not notify the time ending)

        turnNo == int runinng number on starting turn.
        boardSituation == 8*8 list containing containing int [0|1|2] where 0 == enpty, 1 == player1 and 2 == player2.
        validMoves == list containing [x,y] for each place the gamelogic thinks you can make a move to (the list might also be empty).
        makeMoveCallBack == function call, wich you should make your move with. The function accepts 2 parameters int x, y to point your move on the board, or like this example x = [x,y] (list containing the move) and y = None. The function returns True if the move was ok (and done), or False if the move was illegal.
        """
        startTime = time.time() #you can use time -calss to measure your turn length
        self.board = boardSituation

        if len(validMoves):
            if makeMoveCallBack(validMoves[random.randrange(len(validMoves))]):
                #The move was ok
                pass
            else:
                #The move was illegal
                pass
        else:
            print ("Randomizer: No valid moves")
        #print ("turn took: %f" %(time.time()-startTime)) # this 'algorthm' one takes so little time that the turn time is always 0.00 sec.

    def gameEnd(self):
        """Method to call when game round ends.
        It's time to clean up and free any possible reserved recources.
        This function is called also if the game is aborted.
        """
        self.run = False
