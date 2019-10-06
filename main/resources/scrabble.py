from .player import Player
from .cell import Cell


class Scrabble:
    """Главный игровой класс"""

    def _fill_board(self):
        """Заполняет игровое поле начальными значениями"""
        self.board = list()
        for i in range(15):
            self.board.append(list())
            for j in range(15):
                if i == j or i == 14 - j:
                    if j == 0 or j == 14:
                        self.board[i].append(Cell("word", '3w', 3))
                    elif 0 < j < 5 or 9 < j < 14:
                        self.board[i].append(Cell("word", '2w', 2))
                    elif j == 5 or j == 9:
                        self.board[i].append(Cell("letter", '3l', 3))
                    elif j == 6 or j == 8:
                        self.board[i].append(Cell("letter", '2l', 2))
                    else:
                        self.board[i].append(Cell())
                elif i == j - 4 or i == 18 - j:
                    if j == 5 or j == 13:
                        self.board[i].append(Cell("letter", '3l', 3))
                    elif 5 < j < 8 or 10 < j < 13:
                        self.board[i].append(Cell("letter", '2l', 2))
                    else:
                        self.board[i].append(Cell())
                elif i == j + 4 or i == 10 - j:
                    if j == 1 or j == 9:
                        self.board[i].append(Cell("letter", '3l', 3))
                    elif 1 < j < 4 or j == 8:
                        self.board[i].append(Cell("letter", '2l', 2))
                    else:
                        self.board[i].append(Cell())
                elif (i == 7 and (j == 0 or j == 14)) or (j == 7 and (i == 0 or i == 14)):
                    self.board[i].append(Cell("word", '3w', 3))
                elif ((i == 0 or i == 14) and (j == 3 or j == 11)) or ((i == 3 or i == 11) and (j == 0 or j == 14)):
                    self.board[i].append(Cell("letter", '2l', 2))
                else:
                    self.board[i].append(Cell())

    def _get_dict(self):
        """Получение словаря возможных слов"""
        f = open("resources/word_rus.txt", encoding="utf-8")
        self._dict = set(f.read().splitlines())
        f.close()

    def __init__(self):
        self._fill_board()
        self._get_dict()

    def print_board(self):  # TODO: имя и буквы текущего игрока после поля
        for i in range(15):
            for j in range(15):
                print('{:>3}'.format(self.board[i][j].cur_letter), end='')
            print('\n')

    def get_hint(self): # подсказка для игрока куда ставить букву (можно реализовать подсвечивание
        pass            # или вставку буквы или слова на нужное место сразу)

    def check_word(self): # проверяет слово на корректность (в противном случае бросается исключение)
        pass

    def set_word(self): # вставляет слово вызывает (вызывает функцию проверки и тд) и возвращает стоимость слова
        pass
