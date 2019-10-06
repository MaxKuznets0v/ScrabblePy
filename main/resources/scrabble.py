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

    def _set_dict(self):
        """Получение словаря возможных слов"""
        f = open("resources/word_rus.txt", encoding="utf-8")
        self._dict = set(f.read().splitlines())
        f.close()

    def _set_tables(self):
        self._let_price = {'А': 1, 'Б': 3, 'В': 1,
                           'Г': 3, 'Д': 2, 'Е': 1,
                           'Ё': 3, 'Ж': 5, 'З': 5,
                           'И': 1, 'Й': 4, 'К': 2,
                           'Л': 2, 'М': 2, 'Н': 1,
                           'О': 1, 'П': 2, 'Р': 1,
                           'С': 1, 'Т': 1, 'У': 2,
                           'Ф': 10, 'Х': 5, 'Ц': 5,
                           'Ш': 8, 'Щ': 10, 'Ъ': 10,
                           'Ы': 4, 'Ь': 3, 'Э': 8,
                           'Ю': 8, 'Я': 3}

        self._let_amount = {'А': 8, 'Б': 2, 'В': 4,
                            'Г': 2, 'Д': 4, 'Е': 8,
                            'Ё': 1, 'Ж': 1, 'З': 2,
                            'И': 5, 'Й': 1, 'К': 4,
                            'Л': 4, 'М': 3, 'Н': 5,
                            'О': 10, 'П': 4, 'Р': 5,
                            'С': 5, 'Т': 5, 'У': 4,
                            'Ф': 1, 'Х': 1, 'Ц': 1,
                            'Ш': 1, 'Щ': 1, 'Ъ': 1,
                            'Ы': 2, 'Ь': 2, 'Э': 1,
                            'Ю': 1, 'Я': 2}

    def __init__(self):
        self._fill_board()
        self._set_dict()
        self._set_tables()

    def print_board(self):  # TODO: имя и буквы текущего игрока после поля
        for i in range(15):
            for j in range(15):
                print('{:>3}'.format(self.board[i][j].cur_letter), end='')
            print('\n')

    def get_hint(self):  # подсказка для игрока куда ставить букву (можно реализовать подсвечивание
        pass             # или вставку буквы или слова на нужное место сразу)

    def check_word(self, word):  # проверяет слово на корректность (в противном случае бросается исключение)
        if word not in self._dict:
            raise ValueError("Слова " + word + " нет в словаре!")

    def set_word(self):  # вставляет слово вызывает (вызывает функцию проверки и тд) и возвращает стоимость слова
        pass
