#!/usr/bin/python3
# -*- coding: utf-8 -*-

import random, sys, time, math, os
import reversi

class dummyPlayer():
    def __init__(self):
        self.name = None
        self.ui = None
        self.wins = 0
        self.pointsTotal = 0
        self.roundTimeTotal = 0
        self.longestTurn = 0
        self.timeExeeded = 0

class reversiGUI():
    """Reversi game with graphic user interface
    """
    def __init__(self, noMoves = False, noRotate = False, turnTime = 0):
        self.run = 0
        self.pause = False
        self.rotateStarter = not noRotate #rotate the starting player?
        self.noMoves = noMoves #Print moves made to the console?
        self.turnTime = turnTime #Not used yet
        if self.noMoves:
            self.game = reversi.Reversi(None, None)
        else:
            self.game = reversi.Reversi(self.moveMade, None)
        self.startGame = 1
        self.roundsPlayed = 0
        self.lastWinner = 0

        self.pl1 = dummyPlayer()
        self.pl2 = dummyPlayer()

    def startRound(self, pl1, pl2):
        """Round consists of several moves (done by game logic)
        """
        if not self.noMoves:
            print ("\n[turn, player, [x, y]]")
        self.startGame = 0

        #Play the round
        results = self.game.roundStart(pl1.ui, pl2.ui)

        #Save round result to owerall results
        if type(results) == list and len(results) == 5:
            pl1.pointsTotal += results[1]
            pl2.pointsTotal += results[2]
            pl1.roundTimeTotal += results[3]
            pl2.roundTimeTotal += results[4]

            if results[0] == 1:
                print ("Victory to %s with %d-%d tokens" %(pl1.name, results[1], results[2]))
                pl1.wins += 1
            elif results[0] == 2:
                print ("Victory to %s with %d-%d tokens" %(pl2.name, results[2], results[1]))
                pl2.wins += 1
            elif results[0] == -1:
                print ("Draw")
                pl1.wins += 0.5
                pl2.wins += 0.5
        return results[0]

    def startTurnament(self, pl1, pl2, rounds):
        """Turnament consists of 1-n rounds
        Players take turns as a starting player
        """
        #init the ai's
        self.run = 1
        if pl1 != None:
            self.pl1.name = pl1
            self.pl1.ui = __import__(pl1).Game_ai(None)
        if pl2 != None:
            self.pl2.name = pl2
            self.pl2.ui = __import__(pl2).Game_ai(None)

        #Play the rounds
        while self.roundsPlayed < rounds and self.run:
            self.lastWinner = 0
            if self.rotateStarter and self.roundsPlayed%2 == 1:
                print ("\n\nRound %d/%d \n%s vs %s\n" %(self.roundsPlayed+1, rounds, self.pl2.name, self.pl1.name))
                winner = self.startRound(self.pl2, self.pl1)
                if winner == 1:
                    self.lastWinner = 2
                elif winner == 2:
                    self.lastWinner = 1
                else:
                    self.lastWinner = winner
                print ("%s %d - %d %s" %(self.pl1.name, self.pl1.wins, self.pl2.wins, self.pl2.name))
            else:
                print ("\nRound %d/%d \n%s vs %s\n\n" %(self.roundsPlayed+1, rounds, self.pl1.name, self.pl2.name))
                self.lastWinner = self.startRound(self.pl1, self.pl2)
                print ("%s %d - %d %s" %(self.pl1.name, self.pl1.wins, self.pl2.wins, self.pl2.name))
            self.roundsPlayed +=1

        #Print owerall results
        print ("\n\nPlayers:\t%s\t%s" %(self.pl1.name, self.pl2.name))
        print ("wins:\t\t\t%.1f\t%.1f" %(self.pl1.wins, self.pl2.wins))
        print ("avg points/round:\t%.1f\t%.1f" %(float(self.pl1.pointsTotal)/self.roundsPlayed, float(self.pl2.pointsTotal)/self.roundsPlayed))
        print ("avg round time:\t\t%.5f\t%.5f" %(self.pl1.roundTimeTotal/self.roundsPlayed, self.pl2.roundTimeTotal/self.roundsPlayed))

    def moveMade(self, lastMove = None):
        if not self.noMoves and lastMove != None:
            print (lastMove)
        while self.pause:
            time.sleep(0.2)
            self.checkKeyPressed()

if __name__ == '__main__':
    """Arguments to the program: pl1_filename pl2_filename rounds_to_play
    """
    pl1 = pl2 = None
    rounds = 1
    noMoves = noRotate = False
    turnTime = 0
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if arg[0] == "-":
                if arg == "-noMoves":
                    noMoves = True
                elif arg == "-noRotate":
                    noRotate = True
                elif arg[:7] == "-round=":
                    rounds = int(arg[7:])
                    if rounds < 1 or rounds > 1000:
                        print ("Acceptable round ammount: 1-1000")
                        rounds = 1
                elif arg[:6] == "-time=":
                    turnTime = int(arg[6:])
                else:
                    print ("Unknown argument %s" %(arg))
            else:
                try:
                    path = os.path.split(arg)
                    if path[1] != "commandline.py":
                        if path[1] == "humanPlayer.py":
                            print ("\n\n## Human player not supported. Use 'main.py' insted ##\n\n")
                        elif os.path.isfile(path[1]) and pl1 == None:
                            pl1 = path[1]
                        else:
                            pl2 = path[1]
                except:
                    pass

    if pl1 == None:
        pl1 = "ai_randomizer.py"
    if pl2 == None:
        pl2 = "ai_1depth.py"

    #Start the game
    ui = reversiGUI(noMoves, noRotate, turnTime)
    ui.startTurnament(pl1.strip('.py'), pl2.strip('.py'), rounds)
    sys.exit()
