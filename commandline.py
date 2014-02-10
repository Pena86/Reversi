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
    def __init__(self, noMoves = False, noRotate = False):
        self.run = 0
        self.rotateStarter = not noRotate #rotate the starting player?
        self.noMoves = noMoves #Print moves made to the console?
        if self.noMoves:
            self.game = reversi.Reversi(None, None)
        else:
            self.game = reversi.Reversi(self.moveMade, None)
        self.startGame = 1
        self.roundsPlayed = 0

        self.pl1 = dummyPlayer()
        self.pl2 = dummyPlayer()

    def startRound(self, pl1, pl2, turnTime = 0):
        """Round consists of several moves (done by game logic)
        """
        if not self.noMoves:
            print ("[turn, player, [x, y]]")
        self.startGame = 0

        #Play the round
        results = self.game.roundStart(pl1.ui, pl2.ui, turnTime)

        #Save round result to owerall results
        pl1.pointsTotal += results["pl1tiles"]
        pl2.pointsTotal += results["pl2tiles"]
        pl1.roundTimeTotal += results["pl1time"]
        pl2.roundTimeTotal += results["pl2time"]
        if pl1.longestTurn < results["pl1longest"]:
            pl1.longestTurn = results["pl1longest"]
        pl1.timeExeeded += results["pl1err"]
        if pl2.longestTurn < results["pl2longest"]:
            pl2.longestTurn = results["pl2longest"]
        pl2.timeExeeded += results["pl2err"]

        if results["winner"] == 1:
            print ("Victory to %s with %d-%d tokens" %(pl1.name, results["pl1tiles"], results["pl2tiles"]))
            pl1.wins += 1
        elif results["winner"] == 2:
            print ("Victory to %s with %d-%d tokens" %(pl2.name, results["pl2tiles"], results["pl1tiles"]))
            pl2.wins += 1
        elif results["winner"] == -1:
            print ("Draw")
            pl1.wins += 0.5
            pl2.wins += 0.5

        print ("%s longest turn: %.3f with %d time exeedings" %(pl1.name, results["pl1longest"], results["pl1err"]))
        print ("%s longest turn: %.3f with %d time exeedings" %(pl2.name, results["pl2longest"], results["pl2err"]))

        return results["winner"]

    def startTurnament(self, pl1, pl2, rounds, turnTime):
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
            if self.rotateStarter and self.roundsPlayed%2 == 1: #Starter rotation
                roundPl1 = self.pl2
                roundPl2 = self.pl1
            else:
                roundPl1 = self.pl1
                roundPl2 = self.pl2

            print ("\nRound %d/%d \n%s vs %s\n\n" %(self.roundsPlayed+1, rounds, roundPl1.name, roundPl2.name))
            self.startRound(roundPl1, roundPl2, turnTime)
            print ("%s %d - %d %s" %(roundPl1.name, roundPl1.wins, roundPl2.wins, roundPl2.name))
            self.roundsPlayed +=1

        #Print owerall results
        print ("\n\nPlayers:\t%s\t%s" %(self.pl1.name, self.pl2.name))
        print ("wins:\t\t\t%.1f\t%.1f" %(self.pl1.wins, self.pl2.wins))
        print ("avg points/round:\t%.1f\t%.1f" %(float(self.pl1.pointsTotal)/self.roundsPlayed, float(self.pl2.pointsTotal)/self.roundsPlayed))
        print ("avg round time:\t\t%.3f\t%.3f" %(self.pl1.roundTimeTotal/self.roundsPlayed, self.pl2.roundTimeTotal/self.roundsPlayed))
        print ("longest turn: \t\t%.3f\t%.3f" %(self.pl1.longestTurn, self.pl2.longestTurn))
        print ("total time exeedings: \t%d\t%d" %(self.pl1.timeExeeded, self.pl2.timeExeeded))

    def moveMade(self, lastMove = None):
        if not self.noMoves and lastMove != None:
            print (lastMove)

if __name__ == '__main__':
    """
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
    ui = reversiGUI(noMoves, noRotate)
    ui.startTurnament(pl1.strip('.py'), pl2.strip('.py'), rounds, turnTime)
    sys.exit()
