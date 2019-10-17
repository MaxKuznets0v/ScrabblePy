from .cell import Cell
from resources.player import Player
from resources import Utils


class GameBoard:
    """Класс игровой доски"""

    def _fill_board(self):
        """Заполняет игровое поле начальными значениями"""
        self.board = list()
        self.board.append(list())
        self.board[0].append(' ')
        for ch in Utils.y_axis:
            self.board[0].append(ch)

        for i in range(1, 16):
            self.board.append(list())
            self.board[i].append(i)
            for j in range(1, 16):
                if i == j or i == 16 - j:
                    if j == 1 or j == 15:
                        self.board[i].append(Cell("word", '3w', 3))
                    elif 1 < j < 6 or 10 < j < 15:
                        self.board[i].append(Cell("word", '2w', 2))
                    elif j == 6 or j == 10:
                        self.board[i].append(Cell("letter", '3l', 3))
                    elif j == 7 or j == 9:
                        self.board[i].append(Cell("letter", '2l', 2))
                    else:
                        self.board[i].append(Cell())
                elif i == j - 4 or i == 20 - j:
                    if j == 6 or j == 14:
                        self.board[i].append(Cell("letter", '3l', 3))
                    elif 6 < j < 9 or 11 < j < 14:
                        self.board[i].append(Cell("letter", '2l', 2))
                    else:
                        self.board[i].append(Cell())
                elif i == j + 4 or i == 12 - j:
                    if j == 2 or j == 10:
                        self.board[i].append(Cell("letter", '3l', 3))
                    elif 2 < j < 5 or j == 9:
                        self.board[i].append(Cell("letter", '2l', 2))
                    else:
                        self.board[i].append(Cell())
                elif (i == 8 and (j == 1 or j == 15)) or (j == 8 and (i == 1 or i == 15)):
                    self.board[i].append(Cell("word", '3w', 3))
                elif ((i == 1 or i == 15) and (j == 4 or j == 12)) or ((i == 4 or i == 12) and (j == 1 or j == 15)):
                    self.board[i].append(Cell("letter", '2l', 2))
                else:
                    self.board[i].append(Cell())

    def __init__(self):
        self._fill_board()

    def print_board(self):
        print("--------------------------------------------------------")
        for i in range(16):
            print('{:>3}'.format((self.board[0][i])), end='')
        print('\n')

        for i in range(1, 16):
            print('{:>3}'.format(self.board[i][0]), end='')
            for j in range(1, 16):
                print('{:>3}'.format(self.board[i][j].cur_letter), end='')
            print('\n')
