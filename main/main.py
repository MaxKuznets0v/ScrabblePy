"""Главный игровой файл"""
from resources.scrabble import Scrabble
#from resources.cell import Cell
#from resources.player import Player

game = Scrabble()
game.print_board()
game.set_word('звон 8 З u')