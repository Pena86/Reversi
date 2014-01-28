

class Game_ai:
    """Example Ai class
    """
    def __init__(self):
        self.move = (-1,-1)
        self.run = False
        self.board = []
        self.player = -1

    def gameStart(self, playerNo):
        """Method to call when game round starts
        """
        self.run = True
        self.player = playerNo
    
    def makeMove(self, turnNo, boardSituation, validMoves, makeMoveCallBack):
        """Method to call when it's time to make a move
        """
        self.board = boardSituation
        
        changes = {}
        
        for x in range(0,8):
            for y in range(0,8):
                if self.board[x][y] == 0:
                    c = self.place_piece(x, y, live_mode=False)
                    if c > 0:
                        changes[(x,y)] = c
        
        # No moves can be found
        if changes == {}:
            makeMoveCallBack(None, None)
            print ("1depth: No valid moves")
            return
        
        max_key, max_val = (-1,-1), 0
        
        for k, v in changes.items():
            if v > max_val:
                max_key = k
        
        x, y = max_key
        makeMoveCallBack(x, y)

    def gameEnd(self):
        """Method to call when game roun ends
        """
        self.run = False

    def place_piece(self, x, y, live_mode=True):
        if live_mode:
            self.board[x][y] = self.player
        change_count = 0
        
        # Get a reference to the row and column that we just placed a piece on
        column = self.board[x]
        row = [self.board[i][y] for i in range(0,8)]
        
        # First can we travel up?
        if self.player in column[:y]:
            changes = []
            search_complete = False
            
            for i in range(y-1,-1,-1):
                if search_complete: continue
                
                counter = column[i]
                
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append(i)
            
            # Perform changes
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i in changes:
                        self.board[x][i] = self.player
        
        # Down?
        if self.player in column[y:]:
            changes = []
            search_complete = False
            
            for i in range(y+1,8,1):
                if search_complete: continue
                
                counter = column[i]
                
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append(i)
            
            # Perform changes
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i in changes:
                        self.board[x][i] = self.player
        
        # Left?
        if self.player in row[:x]:
            changes = []
            search_complete = False
            
            for i in range(x-1,-1,-1):
                if search_complete: continue
                
                counter = row[i]
                
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append(i)
            
            # Perform changes
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i in changes:
                        self.board[i][y] = self.player
        
        # Right?
        if self.player in row[x:]:
            changes = []
            search_complete = False
            
            for i in range(x+1,8,1):
                if search_complete: continue
                
                counter = row[i]
                
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append(i)
            
            # Perform changes
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i in changes:
                        self.board[i][y] = self.player
        
        # Diagonals are a little harder
        i, j = x-7, y+7
        bl_tr_diagonal = []
        
        for q in range(0, 16):
            if 0 <= i < 8 and 0 <= j < 8:
                bl_tr_diagonal.append(self.board[i][j])
            
            i += 1
            j -= 1
        
        i, j = x-7, y-7
        br_tl_diagonal = []
        for q in range(0, 16):
            
            if 0 <= i < 8 and 0 <= j < 8:
                br_tl_diagonal.append(self.board[i][j])
            
            i += 1
            j += 1
        
        # Up Right
        if self.player in bl_tr_diagonal:
            changes = []
            search_complete = False
            i = 0
            lx, ly = x, y
            
            while 0 <= lx < 8 and 0 <= ly < 8:
                lx += 1
                ly -= 1
                
                if lx > 7 or ly < 0: break
                if search_complete: continue
                
                counter = self.board[lx][ly]
                
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append((lx, ly))
            
            # Perform changes
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i, j in changes:
                        self.board[i][j] = self.player
        
        # Down Left
        if self.player in bl_tr_diagonal:
            changes = []
            search_complete = False
            i = 0
            lx, ly = x, y
            
            while 0 <= lx < 8 and 0 <= ly < 8:
                lx -= 1
                ly += 1
                
                if lx < 0 or ly > 7: break
                if search_complete: continue
                
                counter = self.board[lx][ly]
                
                
                if counter == 0:
                    changes = []
                    search_complete = True
                    break
                elif counter == self.player:
                    search_complete = True
                    break
                else:
                    changes.append((lx, ly))
            
            
            # Perform changes
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i, j in changes:
                        self.board[i][j] = self.player
        
        
        # Up Left
        if self.player in br_tl_diagonal:
            changes = []
            search_complete = False
            i = 0
            lx, ly = x, y
            
            while 0 <= lx < 8 and 0 <= ly < 8:
                lx -= 1
                ly -= 1
                
                if lx < 0 or ly < 0: break
                if search_complete: continue
                
                counter = self.board[lx][ly]
                
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append((lx, ly))
            
            # Perform changes
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i, j in changes:
                        self.board[i][j] = self.player
        
        # Down Right
        if self.player in br_tl_diagonal:
            changes = []
            search_complete = False
            i = 0
            lx, ly = x, y
            
            while 0 <= lx < 8 and 0 <= ly < 8:
                lx += 1
                ly += 1
                
                if lx > 7 or ly > 7: break
                if search_complete: continue
                
                counter = self.board[lx][ly]
                
                if counter == 0:
                    changes = []
                    search_complete = True
                elif counter == self.player:
                    search_complete = True
                else:
                    changes.append((lx, ly))
            
            # Perform changes
            if search_complete:
                change_count += len(changes)
                if live_mode:
                    for i, j in changes:
                        self.board[i][j] = self.player
        
        if change_count == 0 and live_mode:
            self.board[x][y] = 0
            raise Illegal_move("Player {0} tried to place a tile at {1},{2} but that will result in 0 flips".format(
                self.player,
                x, y,
            ))
        
        # if change_count > 0:
        #     print("Tested at {0},{1} and found {2} changes".format(x, y, change_count))
        return change_count
