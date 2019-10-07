"""Главный игровой файл"""
from resources.scrabble import Scrabble
#from resources.cell import Cell
#from resources.player import Player

game = Scrabble()
game.print_board()
print(game.board[10][10].type)