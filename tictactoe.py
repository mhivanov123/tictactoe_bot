import random

class tictactoe():
    def __init__(self):
        self.board = '*'*9
        self.end = False
        self.tie = False

        self.move2index = {'TL': 0, 'TC': 1, 'TR': 2, 'ML': 3, 'MC': 4, 'MR': 5, 'BL': 6, 'BC': 7, 'BR': 8}
        self.index2move = {0: 'TL', 1: 'TC', 2:'TR', 3: 'ML', 4:'MC', 5:'MR', 6: 'BL', 7:'BC', 8: 'BR'}

    def get_available(self):
        return [self.index2move[n] for n in range(9) if self.board[n] == '*']
        
    def move(self,loc,piece):
        self.board = self.board[:self.move2index[loc]] + piece + self.board[self.move2index[loc]+1:] if self.move2index[loc] != 8 else self.board[:self.move2index[loc]] + piece
        self.check(piece)

    def check(self,piece):
        if any([self.board[0] == self.board[3] == self.board[6] == piece,
        self.board[1]==self.board[4]==self.board[7] == piece,
        self.board[2] == self.board[5] == self.board[8] == piece,
        self.board[0]==self.board[1]==self.board[2] == piece,
        self.board[3] == self.board[4] == self.board[5] == piece,
        self.board[6]==self.board[7]==self.board[8] == piece,
        self.board[0] == self.board[4] == self.board[8] == piece,
        self.board[2]==self.board[4]==self.board[6] == piece]):
            self.end = True
        else:
            if all(self.board[n] != '*' for n in range(9)):
                self.end = True  
                self.tie = True

    def __str__(self):
        res = ''
        for index,value in enumerate(list(self.board)):
            res = res + "\033[4m"+value+"\033[0m" if value != '*' else res + '_'
            res = res + '\n' if index%3 == 2 else res + '|'
        return res
    
class ttt_game():
    def __init__(self,game,player1,player2):
        self.game = game
        self.p1 = player1
        self.p2 = player2
        self.order = self.p1.piece
        
    def move_request(self,player):
        """
        ask player to make move
        """
        player.get_move(self.game)

    def play(self):
        """
        continue waking moves until game is over
        """
        while not self.game.end:
            if self.order == self.p1.piece:
                self.move_request(self.p1)
                self.order = self.p2.piece
            elif self.order == self.p2.piece:
                self.move_request(self.p2)
                self.order = self.p1.piece

        else:
            if self.game.tie:
                self.p1.temp.append('tie')
                self.p2.temp.append('tie')
            elif self.order == self.p1.piece:
                self.p1.temp.append('loss')
                self.p2.temp.append('win')
            else:
                self.p2.temp.append('loss')
                self.p1.temp.append('win')

            self.p1.update_memory(self.game)
            self.p2.update_memory(self.game)

class player():
    def __init__(self,piece):
        self.piece = piece
        self.opp = 'X' if piece == 'O' else 'O'
        self.learning_rate = 0.9
        self.eve = 0.2
        self.memory = {}
        self.temp = []

    def get_move(self,board):
        """
        give action to be taken
        """
        s = board.board[:]
        available = board.get_available()

        if random.random() < self.eve and s in self.memory:
            a = max([(key,value) for key,value in self.memory[s].items() if key in available],key = lambda x: x[1])[0]

        else:
            a = random.choice(available)

        board.move(a,self.piece)
        self.temp.append((s,a,board.board[:]))
        

    def update_memory(self,board):
        """
        q learning function. rewards 1 for 
        """
        for n in range(len(self.temp)-1):
            s = self.temp[n][0]
            a = self.temp[n][1]
            s_ = self.temp[n][2]

            if self.temp[n+1] == 'win':
                r = 1
                pred = 0
            elif self.temp[n+1] == 'loss':
                r = -1
                pred = 0
            elif self.temp[n+1] == 'tie':
                r = -1
                pred = 0
            else:
                r = 0
                pred = self.predict_state(s_)
            
            if s in self.memory:         
                if a in self.memory[s]:
                    self.memory[s][a] = (1- self.learning_rate)*self.memory[s][a] + self.learning_rate*(r+pred)
                else:
                    self.memory[s][a] = self.learning_rate*(r + pred)
            else:
                self.memory[s] = {a: self.learning_rate*(r + pred)}

        self.temp = []
        

    def predict_state(self,board):
        def available(board):
            index2move = {0: 'TL', 1: 'TC', 2:'TR', 3: 'ML', 4:'MC', 5:'MR', 6: 'BL', 7:'BC', 8: 'BR'}
            return [index2move[n] for n in range(9) if board[n] == '*']
        
        move2index = {'TL': 0, 'TC': 1, 'TR': 2, 'ML': 3, 'MC': 4, 'MR': 5, 'BL': 6, 'BC': 7, 'BR': 8}

        opts = available(board)
        num_opts = len(opts)
        
        ret = 0
        for move in opts:
            copy_board = board[:]
            copy_board = copy_board[:move2index[move]] + self.opp + copy_board[move2index[move]+1:] if move2index[move] != 8 else copy_board[:move2index[move]] + self.opp
            ret += max(self.memory.get(copy_board,{0:0}).values())

        return ret/num_opts


