from .player import Player
import random
from .cell import Cell


class Scrabble:
    """Главный игровой класс"""

    def _fill_board(self):
        """Заполняет игровое поле начальными значениями"""
        self.board = list()
        self.board.append(list())
        self.board[0].append(' ')
        for ch in 'АБВГДЕЖЗИЙКЛМНО':
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

    def _set_dict(self):
        """Получение словаря возможных слов"""
        f = open("resources/erudit.txt", encoding="utf-8")
        self._dict = set(f.read().split(','))
        f.close()

    def _set_tables(self):
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

    def _init_letters(self):
        """Выставляет буквы игроков при старте"""
        let = list()
        for i in range(7):
            while True:  # не даем взять больше букв, чем имеем
                cur_letter = random.choice(list(self._let_to_amount.keys()))
                if self._let_to_amount[cur_letter] > 0:
                    break
                else:
                    continue
            self._let_to_amount[cur_letter] -= 1
            let.append(cur_letter)
        return let

    def _create_players(self):
        """Создает 2 игроков"""
        name1 = input("Введите имя первого игрока: ")
        name2 = input("Введите имя второго игрока: ")
        self.player_list = [Player(0, name1, self._init_letters()), Player(0, name2, self._init_letters())]

    def __init__(self):  # TODO: выбор режима
        self._fill_board()
        self._set_dict()
        self._set_tables()
        self._create_players()

    def print_board(self):  # TODO: имя и буквы текущего игрока после поля
        for i in range(16):
            print('{:>3}'.format((self.board[0][i])), end='')
        print('\n')

        for i in range(1, 16):
            print('{:>3}'.format(self.board[i][0]), end='')
            for j in range(1, 16):
                print('{:>3}'.format(self.board[i][j].cur_letter), end='')
            print('\n')

    def get_hint(self):  # подсказка для игрока куда ставить букву (можно реализовать подсвечивание
        pass             # или вставку буквы или слова на нужное место сразу)

    def check_word(self, word):  # проверяет слово на корректность (в противном случае бросается исключение)
        if word not in self._dict:
            raise ValueError("Слова " + word + " нет в словаре!")
            #return False
        #return True

    def set_word(self, inp):  # вставляет слово вызывает (вызывает функцию проверки и тд) и возвращает стоимость слова
    # inp - строка, поданная на вход из консоли в формате "word x y u/h", где x и y - координаты начала слова, а u/h - способ выкладки слово(вертикально или горизонтально)
        # посмотрел на доску у своей scrabble, там нумерация ячеек как в морском бое: цифры и буквы и
        # начало координат в левом верхнем углу, предлагаю сделать так же

        try:
            self.check_word(inp)
        except ValueError:
            pass

        word, x, let, way = inp.split() # слово, координаты, способ выкладки
        x = int(x)
        let = let.upper()
        y = ord(let) - 1039  # так как ord('A') = 1039
        word = word.upper()
        count = 0
        modifier = 1
        if way == 'u':
            index = x
            for letter in word:
                cell = self.board[index][y]
                if cell.mod_type == 'word':
                    modifier *= cell.modifier
                count += cell.set_letter(letter)
                index += 1

        else:
            index = y
            for letter in word:
                cell = self.board[x][index]
                if cell.mod_type == 'word':
                    modifier *= cell.modifier
                count += cell.set_letter(letter)
                index += 1

        self.print_board()
        return modifier * count
