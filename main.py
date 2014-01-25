#!python3

import pygame, random, sys, time, math, os
from pygame.locals import *
import reversi, ai, humanPlayer

COUNTER_SIZE = 40
TILE_SIZE = 50
COUNTER_PADDING = 5
FPS = 40

WINDOWWIDTH = TILE_SIZE * 8
WINDOWHEIGHT = TILE_SIZE * 8

class reversiGUI():
    """Reversi game with graphic user interface
    Some of this code is not mine. I have taken some parts from: https://github.com/Teifion/Reversi Thanks to Teifion for good example!
    """
    def __init__(self):
        self.resources = {}
        self.keys = []
        self.game = reversi.Reversi(self.moveMade)
        self.player1 = humanPlayer.Human(self.checkKeyPressed)
        self.player2 = ai.Game_ai()
        self.run = 0

    def startRound(self):
        self.run = 1
        pygame.init()
        self.main_clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Reversi')

        # set up images
        self.resources['board'] = pygame.image.load('media/board.png')
        self.resources['black'] = pygame.image.load('media/black.png')
        self.resources['white'] = pygame.image.load('media/white.png')
        
        self.draw_board()

        self.game.roundStart(self.player1, self.player2)

        pygame.quit()

    def quit(self):
        self.run = 0
        game.abort()

    def newGame(self):
        pass

    def moveMade(self):
        self.draw_board()

    def checkKeyPressed(self):
        self.keys = pygame.key.get_pressed()
        eventList = pygame.event.get()

        if (pygame.K_RCTRL in self.keys or pygame.K_LCTRL in self.keys) and pygame.K_q in self.keys:
            quit()

        if (pygame.K_RCTRL in self.keys or pygame.K_LCTRL in self.keys) and pygame.K_n in self.keys:
            self.newGame()

        for event in eventList:
            if event.type == pygame.QUIT:
                quit()

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
    
    def draw_board(self):
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
            self.drawText("Victory to White", font, self.surface, 38, 10)
        if self.game.winner == 2:
            self.drawText("Victory to Black", font, self.surface, 39, 10)
        
        pygame.display.update()


if __name__ == '__main__':
    ui = reversiGUI()
    ui.startRound()
    sys.exit()
