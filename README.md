I have started to modify this project to my needs. We have a class about AI's and there are a class work that implements a AI to reversi game (http://en.wikipedia.org/wiki/Reversi). The class uses java in default, but I prefer python, so I decided to make my own local game server, in where we can develope and compete with our AI's.
We'll see how this plays out...

Dependancies:  
- Python 3.3.3  
- PyGame 1.9.2a0

The program is run simply with:

    python main.py  

Optional parameters for the game:  

	python main.py [ai1_filename ai2_filename -round=2 -time=0 -noMoves -noRotate]  
	
- ai1- and ai2_filenames tell where to load the competing ai's (Note! for now, the ai files must be on the same folder as other .py files!) (or with 'humanPlayer.py' you can play yourself)  
- '-round=' + integer 1 to 1000, to how many rounds the ai's will play  
- '-time=' + integer in sec, how much AI has time to make a turn. 0 = infinite  
- '-noMoves' Don't print or show the moves, makes program faster to run (but doesn't print the board for hummanPlayer.py neither)  
- '-noRotate' Don't rotate the starting player, so player1 is always the starting player

The program prints some statistic before quit.

Some key commands at the game:  
- Quit: Cmd + Q or Ctrl + q  
- New game: Cmd + N or Ctrl + n  
- Pause game: Ctrl + p


