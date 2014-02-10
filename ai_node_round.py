#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time, random
import helpClass

class Game_ai:
    """Example Ai class.
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

        # Create the first node of the node tree
        self.node = helpClass.Node(turnNo = 1, gameState = helpClass.GameState(board, 1))
        self.currentNode = self.node  # To keep track where the game is going
        self.node.expandAll(1) # Expand the tree 1 level
    
    def makeMove(self, turnNo, boardSituation, validMoves, makeMoveCallBack):
        """Method to call when it's time to make a move.
        """
        self.board = boardSituation

        # Find current game situation from the node tree
        result = self.currentNode.findFromTree(gameBoard = boardSituation)
        if result != None: # The reasarch can return 'None'
            self.currentNode = result # Update the current node tracker
            self.currentNode.deleteSisters() # Release memory from the paths this game didn't go
            if self.currentNode.parent != None:
                self.currentNode.parent.deleteSisters() # and because we and the opponent made a turn, we need to clear both
        else:
            print ("opponent move not found")


        self.currentNode.expandAll(2) # Expand the node tree with 2 levels



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
        self.node = None
        self.currentNode = self.node
