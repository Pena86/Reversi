I have a study project wich includes developing AI to reversi game (http://en.wikipedia.org/wiki/Reversi). The project uses java as default, but I prefer python, so I decided to create this unofficial game server where me and hopefully some other students can make their project to. The coding of the server gets closer to first release, so I need to update the documentation also accordingly. I hope someone will find this useful for something...

If you need to install python 3 along python 2 use this in windows: https://bitbucket.org/vinay.sajip/pylauncher These instructions are written mostly to windows enviroment. Unix users, you know what to do ;)

The performance of the helpClass node tree seems to be quite modest. In my tests the program can count about 3 level of nodes in 1s and 4 levels in 10s. If you come up with better solution, fork the repo, implement your solution and send me a pull request. Good improvements are always welcome!

### Example ai's

'ai_randomizer.py' is an example AI and also contains some information on what you need to run your ai with the game. Just copy the file and modify it to your needs, and then test it with the game.

'ai_node_turn.py' demonstrates how to create new node tree in ewery turn.

'ai_node_round.py' denomstrates how to update single node tree for whole round.

For each ai, you need to implement your own algorithm (for example min-max), for deciding wich move is the best to make.

### commandline.py

Dependancies:  
- Python 3.3.3  

Run the program with:

    commandline.py 

### main.py

Dependancies:  
- Python 3.3.3 (take the 32bit version: http://python.org/download/releases/3.3.3/)  
- PyGame 1.9.2a0 (32bit, compatible with python 3.3: https://bitbucket.org/pygame/pygame/downloads)

Run the program with:

    main.py  

Some key commands at the game:  
- Quit: Cmd + Q or Ctrl + q  
- New game: Cmd + N or Ctrl + n  
- Pause game: Ctrl + p

### Optional parameters for the game:  

	[main.py|commandline.py] [ai1_filename ai2_filename -round=2 -time=0 -noMoves -noRotate]  
	
- ai1- and ai2_filenames tell where to load the competing ai's (Note! for now, the ai files must be on the same folder as other .py files!) (or with 'humanPlayer.py' you can play yourself) The name of the file is the name of the player  
- '-round=' + integer 1 to 1000, to how many rounds the ai's will play  
- '-time=' + integer in sec, how much AI has time to make a turn. 0 = infinite  
- '-noMoves' Don't print or show the moves, makes program faster to run (but doesn't print the board for hummanPlayer.py neither)  
- '-noRotate' Don't rotate the starting player, so player1 is always the starting player

The program prints some statistic before quit.

### TODO:
- Possible threading for the players  
- Tournament mode  
- Improve the node creation performance




