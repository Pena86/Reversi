#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time, random
import helpClass

class Game_ai:
    """Example Ai class. Make a copy of this file and modify it as your needs to create yur own AI.
    """
    def __init__(self, turnTime = 0, checkButtons = None):
        """Init of the class
        """
        self.move = (-1,-1)
        self.run = False
        self.board = []
        self.player = -1
        self.turnTime = turnTime

    def gameStart(self, playerNo, board = None):
        """Method to call when game round starts.
        """
        self.run = True
        self.player = playerNo
    
    def makeMove(self, turnNo, boardSituation, validMoves, makeMoveCallBack):
        """Method to call when it's time to make a move.
        """
        self.board = boardSituation

        #Create new node at current game situation
        node = helpClass.Node(gameState = helpClass.GameState(boardSituation, self.player), turnNo = turnNo)

        node.expandAll(3) #Expand the node for 3 levels

        #Your min-max algorithm goes here


        if len(validMoves):
            if makeMoveCallBack(validMoves[random.randrange(len(validMoves))]): #This example does an random move
                #The move was ok
                pass
            else:
                #The move was illegal
                pass
        else:
            print ("Test_ai: No valid moves", validMoves)

    def gameEnd(self):
        """Method to call when game round ends.
        """
        self.run = False
