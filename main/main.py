"""Главный игровой файл"""
from resources.gameboard import GameBoard
import random
from resources.cell import Cell
from resources.player import Player


class Scrabble:
    """Основной игровой класс"""
    def _set_bag(self):
        """Инициализация таблицы количества букв"""
        self._let_to_amount = {'А': 8, 'Б': 2, 'В': 4,
                               'Г': 2, 'Д': 4, 'Е': 8,
                               'Ё': 1, 'Ж': 1, 'З': 2,
                               'И': 5, 'Й': 1, 'К': 4,
                               'Л': 4, 'М': 3, 'Н': 5,
                               'О': 10, 'П': 4, 'Р': 5,
                               'С': 5, 'Т': 5, 'У': 4,
                               'Ф': 1, 'Х': 1, 'Ц': 1,
                               'Ш': 1, 'Щ': 1, 'Ъ': 1,
                               'Ы': 2, 'Ь': 2, 'Э': 1,
                               'Ю': 1, 'Я': 2, ' ': 2}

    def _create_players(self):
        """Создает 2 игроков"""
        name1 = input("Введите имя первого игрока: ")
        name2 = input("Введите имя второго игрока: ")
        self.player_list = [Player(0, name1, self._let_to_amount), Player(0, name2, self._let_to_amount)]
        self.turn = random.randint(0, len(self.player_list))  # текущий ход игрока turn - индекс игрока в списке

    def _next_turn(self):
        """Передает ход следующему игроку"""
        self.turn = (self.turn + 1) % len(self.player_list)

    def __init__(self):
        self.board = GameBoard()
        self._set_bag()
        self._create_players()



game = Scrabble()

game.board.print_board(game.player_list[0])
game.board.set_word("звон 1 Б u", game.player_list[0])
