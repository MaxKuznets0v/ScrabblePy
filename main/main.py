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
        self._amount_of_letters = 103

    def _create_players(self):
        """Создает 2 игроков"""
        name1 = input("Введите имя первого игрока: ")
        name2 = input("Введите имя второго игрока: ")
        self.player_list = [Player(0, name1, self._let_to_amount), Player(0, name2, self._let_to_amount)]
        self.turn = random.randint(0, len(self.player_list) - 1)  # текущий ход игрока turn - индекс игрока в списке
        self._amount_of_letters -= 14

    def _next_turn(self):
        """Передает ход следующему игроку"""
        self.turn = (self.turn + 1) % len(self.player_list)

    def _make_turn(self, cur_player):
        """Совершает ход, защитывает очки и переводит ход"""
        while True:
            try:
                inp = input("Ваш ход:")
                if inp.lower() == "правила":  # выводит правила по необходимости
                    self.show_rules()
                    continue
                elif inp.lower() == "пас":  # пропуск хода
                    self._next_turn()
                    break
                cur_player.score += self.board.set_word(inp, cur_player)
                if self._amount_of_letters > 0:  # если в мешочке есть буквы, то выдадим их игроку и запомним новое число букв в мешочке
                    self._amount_of_letters = cur_player.take_letters(self._let_to_amount, self._amount_of_letters)
                self._next_turn()
                break
            except TypeError as er:
                print(er)
            except ValueError as er:
                print(er)
            except Exception:
                print("Что-то пошло не так")

    def __init__(self):
        self.board = GameBoard()
        self._set_bag()
        self._create_players()
        self.main()

    def show_rules(self):  # TODO: правила
        print("Правила:")
        print("Здесь можно расписать правила")
        print("Каждый ход совершается в следующем формате(без кавычек):\n'слово число(1-15) буквы(А-О) режим вставки(u/h)'")
        print("Здесь u - вертикальная вставка сверху вниз, h - гороизонтальная справа налево, буквы А-О, без Ё")

    def main(self):  # TODO: критерий остановки
        playing = True
        self.show_rules()
        while playing:
            player = self.player_list[self.turn]
            self.board.print_board(player)
            self._make_turn(player)
        # По окончанию игры сравнить баллы и вывести на экран имя победителя

game = Scrabble()