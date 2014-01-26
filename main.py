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
    """
    def __init__(self):
        self.resources = {}
        self.keys = []
        self.game = reversi.Reversi(self.moveMade)
        self.player1 = humanPlayer.Human(self.checkKeyPressed)
        self.player2 = ai.Game_ai()
        self.run = 0
        self.startGame = 1

        self.surface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        pygame.display.set_caption('Reversi')

        # set up images
        self.resources['board'] = pygame.image.load('media/board.png')
        self.resources['black'] = pygame.image.load('media/black.png')
        self.resources['white'] = pygame.image.load('media/white.png')

    def startRound(self):
        print ("[turn, player, [x, y]]")
        self.startGame = 0
        self.run = 1
        self.main_clock = pygame.time.Clock()

        self.game.roundStart(self.player1, self.player2)
        self.draw_board()

        while self.run:
            time.sleep(0.1)
            self.checkKeyPressed()

    def quit(self):
        self.run = 0
        self.game.abort()

    def newGame(self):
        self.startGame = 1
        self.run = 0
        self.game.abort()

    def moveMade(self):
        if len(self.game.movesMade) > 0:
            print (self.game.movesMade[-1])
        self.draw_board()

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
    pygame.init()
    while ui.startGame:
        ui.startRound()
    pygame.quit()
    sys.exit()
