from tictactoe import tictactoe,ttt_game,player
import json

p1 = player('X')
p2 = player('O')

for n in range(100000):
  board = tictactoe()
  game = ttt_game(board,p1,p2)
  game.play()

  board = tictactoe()
  game = ttt_game(board,p2,p1) 
  game.play()

  if n%5000 == 0:
      p1.eve = n/100000
      p2.eve = n/100000

for state in p1.memory:
    p1.memory[state] = max([(key,value) for key,value in p1.memory[state].items()],key = lambda x: x[1])[0]

out_file = open("tictactoe_optimal.json", "w") 
json.dump(p1.memory, out_file, indent = 6) 
out_file.close()
