#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy

class Node:
    """Class to store gameStates to a tree
    """
    def __init__(self, parent = None, move = None, gameState = None, turnNo = 1):
        self.parent = parent
        self.childrens = []
        self.moveLedTo = move   #(pl, x, y)
        self.gameState = gameState
        self.turnNo = turnNo

    def delete(self):
        """Deletes the node and all following generations
        """
        for child in self.childrens:
            if child.childrens == []:
                child.parent = None
            else:
                child.delete()
        self.childrens = []

    def deleteSisters(self):
        """Deletes 'sister' nodes, but not itself
        """
        if self.parent != None:
            deleted = []
            for sister in self.parent.childrens:
                #print (sister, self)
                if sister != self:
                    sister.delete()
                    deleted.append(sister)
            for item in deleted:
                self.parent.childrens.remove(item)
        else:
            print ("In a first parent node")

    def moveTo(self, pos):
        """Makes a move to pos = [x, y] and creates a new node as a children
        """
        if type(self.turnNo) == int:
            turnNo = self.turnNo+1
        else:
            print ("Error: Unknown turn number")
            return []
        newGameState = self.gameState.moveTo(pos)
        if newGameState:
            self.childrens.append(type(self)(parent = self, move = (self.gameState.playerTurn, pos[0], pos[1]), gameState = newGameState, turnNo = turnNo))
            return self.childrens[-1]
        else:
            print ("Error: Failed to make a move")
            return []


    def expandAll(self, levels):
        """Expands the node tree with 'levels' = int time
        """
        allChildrens = []
        for x in range(0,levels):
            allChildrens.append(self.expandOneMore())
        return allChildrens

    def expandOneMore(self):
        """Expands the node tree one level
        """
        if self.childrens: #empyt list == False
            total = []
            for child in self.childrens:
                total.extend(child.expandOneMore())
            return total
        else:
            for move in self.gameState.possibleMoves:
                self.moveTo(move)
            return self.childrens

    def printAll(self):
        """Method for debugging
        """
        print (self.turnNo, self.parent, self.childrens, self.moveLedTo, self.gameState)
        self.gameState.printAll()
        for c in self.childrens:
            print ("\n\nChildren")
            c.printAll()


class GameState:
    """Class that represents a reversi game situation
    """
    def __init__(self, board = None, turn = None):
        #print ("gameState init", type(board), turn)
        self.gameBoard = board
        self.playerTurn = turn
        self.disksOnBoard = gameOperations.countTiles(board) #(empty, white, black)
        self.possibleMoves = gameOperations.checkIsValidMoves(turn, board)

    def printBoard(self):
        """More readable print of the board
        """
        board = ""
        for x in self.gameBoard:
            for y in x:
                board = board + str(y) + " "
            board += "\n"
        print (board)

    def moveTo(self, pos):
        """returns new gameState with move done
        """
        if self.playerTurn == 1:
            turn = 2
        else:
            turn = 1
        newBoard = gameOperations.validMove(pos[0], pos[1], self.playerTurn, copy.deepcopy(self.gameBoard))
        if newBoard:
            return type(self)(board = newBoard, turn = turn)
        else:
            print ("Error: Illegal move")
            return False

    def printAll(self):
        """Method for debugging
        """
        print (self.gameBoard, self.playerTurn, self.disksOnBoard, self.possibleMoves)


class GameOperations:
    def __init__(self):
        pass

    def validMove(self, x, y, player, board):
        """If the move is valid, it's made to the board and return new board
            else return False
            x,y = -1,-1 -> 'pass move'
        """
        if player == 1:
            opponent = 2
        elif player == 2:
            opponent = 1
        else:
            print ("--- No player ---")
            return False
        #print (player, opponent, x, y)

        if x == -1 and y == -1 and self.checkIsValidMoves(player, board) == []:
            return board

        piecesToFlip = []
        directionsToCheck = [[0,-1],[1,-1],[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1]]
        for direction in directionsToCheck:
            piecesToFlip.extend(self.checkDirection(x, y, direction[0], direction[1], player, opponent, board))
        #print (piecesToFlip)

        if len(piecesToFlip) > 0:
            board[x][y] = player
            for spot in piecesToFlip:
                board[spot[0]][spot[1]] = player
            return board
        print ("--- Invalid move! ---")
        return False

    def checkDirection(self, x, y, dx, dy, player, opponent, board):
        """Checks pieces to flip in the given direction and return a list of lists for those pieces to flip.
            else return empty list
        """
        x += dx
        y += dy
        foundOpp = []
        while x < 8 and x > -1 and y < 8 and y > -1:
            #print (x, y, len(foundOpp))
            if board[x][y] == opponent:
                foundOpp.append([x,y])
                #print (foundOpp)
            elif len(foundOpp) > 0 and board[x][y] == player:
                #print ("found own")
                return foundOpp
            else:
                return []

            x += dx
            y += dy
        return []

    def checkIsValidMoves(self, player, board):
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
                if board[x][y] == 0:
                    for direction in directionsToCheck:
                        #print (x,y, directionsToCheck.index(direction))
                        if self.checkDirection(x, y, direction[0], direction[1], player, opponent, board) != []:
                            moves.append([x,y])
                            #print ("found")
                            break
        return moves

    def countTiles(self, board):
        """Counts the tiles on the board
        """
        allTiles = [item for sublist in board for item in sublist]
        
        emptyTiles = sum(1 for tile in allTiles if tile == 0)
        whiteTiles = sum(1 for tile in allTiles if tile == 1)
        blackTiles = sum(1 for tile in allTiles if tile == 2)
        return (emptyTiles, whiteTiles, blackTiles)


try:
    gameOperations
except:
    gameOperations = GameOperations()

