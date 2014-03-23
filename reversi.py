#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time, copy

class Reversi:
    """Reversi game logig class
    """
    def __init__(self, movesCallBack = None, buttonsCheck = None):
        self.movesCallBack = movesCallBack
        self.buttonsCheck = buttonsCheck

        self.emptyTiles = 0
        self.whiteTiles = 0
        self.blackTiles = 0

        self.player1 = None
        self.player2 = None

    def roundStart(self, pl1, pl2, turnTime = 0):
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

        self.player1.gameStart(1, self.board)
        self.player2.gameStart(2, self.board)

        if self.movesCallBack != None:
            self.movesCallBack()

        self.turnStart = self.turnLength = self.pl1time = self.pl2time = self.pl1longestTurn = self.pl2longestTurn = self.pl1timeExeeded = self.pl2timeExeeded = 0

        while self.run:
            #time.sleep(0.2)
            validMoves = self.checkIsValidMoves(self.player)

            if self.player == 1:
                self.turnStart = time.time()
                self.player1.makeMove(self.turn, copy.deepcopy(self.board), validMoves, self.moveTo)
                self.turnLength = time.time() - self.turnStart
                self.moveMade(validMoves)
                self.pl1time += self.turnLength
                if turnTime and self.turnLength > turnTime:
                    self.pl1timeExeeded += 1
                if self.pl1longestTurn < self.turnLength:
                    self.pl1longestTurn = self.turnLength
                self.player = 2
                self.turn += 1
            else:
                self.turnStart = time.time()
                self.player2.makeMove(self.turn, copy.deepcopy(self.board), validMoves, self.moveTo)
                self.turnLength = time.time() - self.turnStart
                self.moveMade(validMoves)
                self.pl2time += self.turnLength
                if turnTime and self.turnLength > turnTime:
                    self.pl2timeExeeded += 1
                if self.pl2longestTurn < self.turnLength:
                    self.pl2longestTurn = self.turnLength
                self.player = 1
                self.turn += 1

            self.winner = self.checkGameEnd()

            if self.movesCallBack != None:
                if len(self.movesMade) > 0:
                    self.movesCallBack(self.movesMade[-1])
                else:
                    self.movesCallBack()

            if self.winner:
                self.run = False
                self.player1.gameEnd()
                self.player2.gameEnd()

            if self.buttonsCheck != None:
                self.buttonsCheck()

        #print (self.pl1time, self.pl2time)

        return {"winner": self.winner, "pl1tiles": self.whiteTiles, "pl2tiles": self.blackTiles, \
            "pl1time": self.pl1time, "pl2time": self.pl2time, \
            "pl1longest": self.pl1longestTurn, "pl2longest": self.pl2longestTurn, \
            "pl1err": self.pl1timeExeeded, "pl2err": self.pl2timeExeeded}

    def moveMade(self, validMoves):
        """Update the moves list with 'skip' moves
        """
        if len(validMoves) == 0 and self.movesMade[-1][0] != self.turn:
            self.movesMade.append([self.turn, self.player, [-1,-1]])
        elif len(validMoves) != 0 and len(self.movesMade) > 0 and self.movesMade[-1][0] != self.turn:
            print ("## Player skipped a move, while he could make a move ##")
            self.movesMade.append([self.turn, self.player, [-2,-2]])

    def moveTo(self, x, y = None):
        """Method for players to call when making a move in the game
        """
        if type(x) == list:
            y = x[1]
            x = x[0]

        if x != None and y != None and self.board[x][y] == 0 and self.validMove(x, y, self.player):
            self.movesMade.append([self.turn, self.player, [x,y]])
            return True
        return False

    def getGameBoard(self):
        return self.board

    def abort(self):
        """If the game needs to be aborted at the middle
        """
        self.run = False
        if self.player1 != None:
            self.player1.gameEnd()
        if self.player2 != None:
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
        """Checks pieces to flip in the given direction and return a list of lists for those pieces to flip.
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
        """
        allTiles = [item for sublist in self.board for item in sublist]
        
        self.emptyTiles = sum(1 for tile in allTiles if tile == 0)
        self.whiteTiles = sum(1 for tile in allTiles if tile == 1)
        self.blackTiles = sum(1 for tile in allTiles if tile == 2)
        if not (self.emptyTiles and self.whiteTiles and self.blackTiles) or (len(self.movesMade) > 1 and self.movesMade[-1][2] == [-1,-1] and self.movesMade[-2][2] == [-1,-1]):
            if self.whiteTiles > self.blackTiles: #pl1 has won
                return 1
            elif self.whiteTiles < self.blackTiles: #pl2 has won
                return 2
            else:                           #draw
                return -1
        return False

    def checkIsValidMoves(self, player):
        """Check if there are valid moves for the player
        """
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
