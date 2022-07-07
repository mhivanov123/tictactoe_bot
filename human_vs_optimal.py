from tictactoe import tictactoe
import json

class human_game():
    def __init__(self):
        self.game = tictactoe()
        with open('tictactoe_optimal.json', 'r') as f:
            self.strategy = json.load(f)

    def setup(self):
        print('\n\nCOMPUTER IS "X" AND HUMAN IS "O"')
        order = input('DO YOU WANT TO GO 1ST(1) OR 2ND(2): ')
        self.order = 'O' if order == '1' else 'X'
        print('GOODLUCK')

    def move_request(self):
        """
        ask player to make move
        """
        available_moves = self.game.get_available()
        mov = ''

        while mov not in available_moves:
            mov = input('YOUR TURN. AVAILABLE MOVES: ' + str(available_moves)+ '  ')
            if mov not in available_moves:
                print('TRY AGAIN YOU MELON\n')

        self.game.move(mov,'O')

    def play(self):
        """
        continue waking moves until game is over
        """
        self.setup()
        while not self.game.end:
            print(self.game)
            if self.order == 'O':
                self.move_request()
                self.order = 'X'
            elif self.order == 'X':
                self.game.move(self.strategy[self.game.board],'X')
                self.order = 'O'
        else:
            print(self.game)
            if self.game.tie:
                print('TIE')
            else:
                print('LOSS')

