#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pygame, random, sys, time, math, os
from pygame.locals import *
import reversi, ai_1depth, humanPlayer, ai_randomizer

COUNTER_SIZE = 40
TILE_SIZE = 50
COUNTER_PADDING = 5
FPS = 40

WINDOWWIDTH = TILE_SIZE * 8
WINDOWHEIGHT = TILE_SIZE * 8

class dummyPlayer():
    def __init__(self):
        self.name = None
        self.ui = None
        self.wins = 0
        self.pointsTotal = 0
        self.roundTimeTotal = 0

class reversiGUI():
    """Reversi game with graphic user interface
    """
    def __init__(self):
        self.resources = {}
        self.keys = []
        self.game = reversi.Reversi(self.moveMade, self.checkKeyPressed)
        self.run = 0
        self.startGame = 1
        self.roundsPlayed = 0

        self.pl1 = dummyPlayer()
        self.pl2 = dummyPlayer()

        self.surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Reversi')

        # set up images
        self.resources['board'] = pygame.image.load('media/board.png')
        self.resources['black'] = pygame.image.load('media/black.png')
        self.resources['white'] = pygame.image.load('media/white.png')

    def startRound(self):
        """Round consists of several moves (sone by game logic)
        """
        print ("[turn, player, [x, y]]")
        self.startGame = 0

        #Play the round
        results = self.game.roundStart(self.pl1.ui, self.pl2.ui)
        self.drawBoard()

        #Save round result to owerall results
        if self.game.winner and type(results) == list and len(results) == 4:
            self.pl1.pointsTotal += results[0]
            self.pl2.pointsTotal += results[1]
            self.pl1.roundTimeTotal += results[2]
            self.pl2.roundTimeTotal += results[3]

            if self.game.winner == 1:
                print ("Victory to %s with %d-%d tokens" %(self.pl1.name, results[0], results[1]))
                self.pl1.wins += 1
            elif self.game.winner == 2:
                print ("Victory to %s with %d-%d tokens" %(self.pl2.name, results[1], results[0]))
                self.pl2.wins += 1
            elif self.game.winner == -1:
                print ("Draw")
                self.pl1.wins += 0.5
                self.pl2.wins += 0.5
        print ("%s %d - %d %s" %(self.pl1.name, self.pl1.wins, self.pl2.wins, self.pl2.name))

    def startTurnament(self, pl1, pl2, rounds):
        """Turnament consists of 1-n rounds
        """
        #init the ai's
        self.run = 1
        if pl1 != None:
            self.pl1.name = pl1
            self.pl1.ui = __import__(pl1).Game_ai()
        if pl2 != None:
            self.pl2.name = pl2
            self.pl2.ui = __import__(pl2).Game_ai()

        #Play the rounds
        while self.roundsPlayed < rounds and self.run:
            print ("\nRound %d/%d \n%s vs %s\n\n" %(self.roundsPlayed+1, rounds, self.pl1.name, self.pl2.name))
            self.startRound()
            self.roundsPlayed +=1

        #Print owerall results
        print ("\n\nPlayers:\t%s\t%s" %(self.pl1.name, self.pl2.name))
        print ("wins:\t\t\t%.1f\t%.1f" %(self.pl1.wins, self.pl2.wins))
        print ("avg points/round:\t%.1f\t%.1f" %(float(self.pl1.pointsTotal)/self.roundsPlayed, float(self.pl2.pointsTotal)/self.roundsPlayed))
        print ("avg round time:\t\t%.5f\t%.5f" %(self.pl1.roundTimeTotal/self.roundsPlayed, self.pl2.roundTimeTotal/self.roundsPlayed))

        #whait to quit
        while self.run:
            time.sleep(0.1)
            self.checkKeyPressed()

    def quit(self):
        self.run = 0
        self.game.abort()

    def newGame(self):
        # TODO: check how this now oprates...
        self.startGame = 1
        self.run = 0
        self.game.abort()

    def moveMade(self):
        if len(self.game.movesMade) > 0:
            print (self.game.movesMade[-1])
        self.drawBoard()

    def checkKeyPressed(self):
        self.keys = pygame.key.get_pressed()
        eventList = pygame.event.get()

        for event in eventList:
            if event.type == KEYDOWN:
                # Cmd + Q
                if event.key == 113 and self.keys[310]:
                    self.quit()
                
                # Cmd + N
                if event.key == 106 and self.keys[310]:
                    self.newGame()

                if event.key == pygame.K_q and (self.keys[pygame.K_RCTRL] or self.keys[pygame.K_LCTRL]):
                    self.quit()

                if event.key == pygame.K_n and (self.keys[pygame.K_RCTRL] or self.keys[pygame.K_LCTRL]):
                    self.newGame()

            if event.type == pygame.QUIT:
                self.quit()

            if event.type == MOUSEBUTTONUP:
                x, y = event.pos
                tx = int(math.floor(x/TILE_SIZE))
                ty = int(math.floor(y/TILE_SIZE))
                if not self.game.moveTo(tx, ty):
                    print ("Wrong move")
                else:
                    return True
        return False
    
    def drawText(self, text, font, surface, x, y):
        textobj = font.render(text, 1, (0,0,0))
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
    
    def drawBoard(self):
        # First the board
        the_board = pygame.Rect(0, 0, WINDOWWIDTH, WINDOWHEIGHT)
        self.surface.blit(self.resources['board'], the_board)
        
        # Now the tiles
        for x in range(0, 8):
            for y in range(0, 8):
                player = self.game.board[x][y]
                counter = pygame.Rect(x * TILE_SIZE + COUNTER_PADDING, y * TILE_SIZE + COUNTER_PADDING, COUNTER_SIZE, COUNTER_SIZE)
                
                if player == 1:
                    self.surface.blit(self.resources['white'], counter)
                elif player == 2:
                    self.surface.blit(self.resources['black'], counter)
        
        # Has a victory occurred?
        font = pygame.font.SysFont("Helvetica", 48)
        if self.game.winner == -1:
            self.drawText("Stalemate", font, self.surface, 95, 10)
        if self.game.winner == 1:
            self.drawText("Victory to "+self.pl1.name, font, self.surface, 38, 10)
        if self.game.winner == 2:
            self.drawText("Victory to "+self.pl2.name, font, self.surface, 39, 10)
        
        pygame.display.update()


if __name__ == '__main__':
    """Arguments to the program: pl1_filename pl2_filename rounds_to_play
    """
    pl1 = pl2 = None
    rounds = 1
    if len(sys.argv) > 1:
        for arg in sys.argv:
            try:
                rounds = int(arg)
                if rounds < 1 or rounds > 1000:
                    print ("Acceptable round ammount: 1-1000")
                    rounds = 1
            except:
                try:
                    path = os.path.split(arg)
                    if path[1] != "main.py":
                        if os.path.isfile(path[1]) and pl1 == None:
                            pl1 = path[1]
                        else:
                            pl2 = path[1]
                    pass
                except:
                    pass

    if pl1 == None:
        pl1 = "ai_randomizer.py"
    if pl2 == None:
        pl2 = "ai_1depth.py"

    #Start the game
    ui = reversiGUI()
    pygame.init()
    ui.startTurnament(pl1.strip('.py'), pl2.strip('.py'), rounds)
    pygame.quit()
    sys.exit()
