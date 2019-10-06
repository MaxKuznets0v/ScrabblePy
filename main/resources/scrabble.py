from .player import Player
from .cell import Cell


class Scrabble:
    """Главный игровой класс"""
    # !решить как загружать бд со словами!
    def __init__(self): # заставляет поле ячейками с дефолтным значением (не знаю пока какое взять)
        self.board = []      # и где-то здесь же выбор режима игры
        for i in range(15):
            self.board.append([])
            for j in range(15):
                if i == j or i == 14 - j:
                    if j == 0 or j == 14:
                        self.board[i].append(Cell(letter='3w', mod='3w'))
                    elif 0 < j < 5 or 9 < j < 14:
                        self.board[i].append(Cell(letter='2w', mod='2w'))
                    elif j == 5 or j == 9:
                        self.board[i].append(Cell(letter='3l', mod='3l'))
                    elif j == 6 or j == 8:
                        self.board[i].append(Cell(letter='2l', mod='2l'))
                    else:
                        self.board[i].append(Cell())
                elif i == j - 4 or i == 18 - j:
                    if j == 5 or j == 13:
                        self.board[i].append(Cell(letter='3l', mod='3l'))
                    elif 5 < j < 8 or 10 < j < 13:
                        self.board[i].append(Cell(letter='2l', mod='2l'))
                    else:
                        self.board[i].append(Cell())
                elif i == j + 3 or i == 10 - j:
                    if j == 1 or j == 9:
                        self.board[i].append(Cell(letter='3l', mod='3l'))
                    elif 1 < j < 4 or j == 8:
                        self.board[i].append(Cell(letter='2l', mod='2l'))
                    else:
                        self.board[i].append(Cell())
                elif (i == 7 and (j == 0 or j == 14)) or (j == 7 and (i == 0 or i == 14)):
                    self.board[i].append(Cell(letter='3w', mod='3w'))
                elif ((i == 0 or i == 14) and (j == 3 or j == 11)) or ((i == 3 or i == 11) and (j == 0 or j == 14)):
                    self.board[i].append(Cell(letter='2l', mod='2l'))
                else:
                    self.board[i].append(Cell())

    def print_board(self): # выводит игровое поле, имя игрока, чей сейчас ход и его буквы
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
