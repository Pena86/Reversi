I have a study project wich includes developing AI to reversi game (http://en.wikipedia.org/wiki/Reversi). The project uses java as default, but I prefer python, so I decided to create this unofficial game server where me and hopefully some other students can make their project to. The coding of the server gets closer to first release, so I need to update the documentation also accordingly. I hope someone will find this useful for something...

If you need to install python 3 along python 2 use this in windows: https://bitbucket.org/vinay.sajip/pylauncher These instructions are written mostly to windows enviroment. Unix users, you know what to do ;)

The performance of the helpClass node tree seems to be quite modest. In my tests the program can count about 3 level of nodes in 1s and 4 levels in 10s. If you come up with better solution, fork the repo, implement your solution and send me a pull request. Good improvements are always welcome!

### Example ai's

'ai_randomizer.py' is an example AI and also contains some information on what you need to run your ai with the game. Just copy the file and modify it to your needs, and then test it with the game.

'ai_node_turn.py' demonstrates how to create new node tree in ewery turn.

For each ai, you need to implement your own algorithm (for example min-max), for deciding wich move is the best to make.

### main.py

Dependancies:  
- Python 3.3.3 (take the 32bit version: http://python.org/download/releases/3.3.3/)  
- (optional) PyGame 1.9.2a0 (32bit, compatible with python 3.3: https://bitbucket.org/pygame/pygame/downloads)

Run the program with:

    main.py  

### Optional parameters for the game:  

	main.py [ai1_filename ai2_filename -round=2 -time=0 -noMoves -noRotate -noGui]  
	
- ai1- and ai2_filenames tell where to load the competing ai's (Note! for now, the ai files must be on the same folder as other .py files!) (or with 'humanPlayer.py' you can play yourself) The name of the file is the name of the player  
- '-round=' + integer 1 to 1000, to how many rounds the ai's will play  
- '-time=' + integer in sec, how much AI has time to make a turn. 0 = infinite  
- '-noMoves' Don't print or show the moves, makes program faster to run (but doesn't print the board for hummanPlayer.py neither)  
- '-noRotate' Don't rotate the starting player, so player1 is always the starting player
- '-noGui' Do not use pyGame gui.

Run in windows example:

    main.py -time=1 -round=2 ai_randomizer.py ai_node_turn.py

Run in linux example:

    python3 main.py -time=1 -round=2 ai_randomizer.py ai_node_turn.py

In the examples above, you can replace either one of the AI's with your own AI file to run it.

The program prints some statistic before quit.

### TODO:
- Possible threading for the players  
- Tournament mode  
- Improve the node creation performance




