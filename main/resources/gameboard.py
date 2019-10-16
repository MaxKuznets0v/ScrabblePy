from .cell import Cell
from resources.player import Player


class GameBoard:
    """Класс игровой доски"""

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

    def __init__(self):
        self._fill_board()
        self._set_dict()

    def print_board(self, cur_player):
        print("--------------------------------------------------------")
        for i in range(16):
            print('{:>3}'.format((self.board[0][i])), end='')
        print('\n')

        for i in range(1, 16):
            print('{:>3}'.format(self.board[i][0]), end='')
            for j in range(1, 16):
                print('{:>3}'.format(self.board[i][j].cur_letter), end='')
            print('\n')
        print("Буквы " + cur_player.get_name() + ":")
        print(*cur_player.letters, sep="__")

    def get_hint(self):  # подсказка для игрока куда ставить букву (можно реализовать подсвечивание
        pass  # или вставку буквы или слова на нужное место сразу)

    def check_word(self, inp, cur_player):  # TODO: параллельный ввод
        # проверяет на формат: (слово, x, буква, способ выкладки) пример: "сосна 11 О u" иначе бросить исключение
        # TypeError само слово на корректность (есть ли слово в словаре, не выезжает ли оно за границы,
        # есть ли нужные буквы для этого слова у пользователя, пересекает ли оно необходимые буквы и тд,
        # иначе бросаем ValueError
        """Проверка ввода пользователя на корректность"""
        #проверим, что на вход получили 4 значения
        words = inp.split()
        if len(words) != 4:
            raise TypeError("Введено отличное от 4 количество слов(слово, x, буква, способ выкладки)")

        # проверим что x и буква не выходят за пределы игрового поля
        word, x, y, way = words
        y = y.upper()
        if x.isdigit() and y in 'АБВГДЕЖЗИЙКЛМНО':
            x = int(x)
            y = ord(y.upper()) - 1039
            if 1 > x or x > 15 and 1 > y or y > 15:
                raise TypeError("Введенные координаты выходят за границу игрового поля(1-15, А-О)")

        # проверим что последний параметр u/h
        way = way.lower()
        if way != 'h' and way != 'u':
            raise TypeError("Выбрано неверное направление(u/h)")

        # проверим, что слово есть в словаре
        if word.lower() not in self._dict:
            raise ValueError("Слова " + word.upper() + " нет в словаре")
        word = word.upper()
        # проверим, что слово не выходит за край, если выполнено проверяем остальное
        used_letters = list()  # у игрока могут быть не все необходимые буквы, главное, чтобы они лежали на поле
        f = False  # флаг, отвечающий за проверку того, что хотя бы раз было пересечено уже выложенное на доске слово
        if way == 'u':
            if x + len(word) < 15:
                for i in range(len(word)):
                    letter = self.board[x + i][y].cur_letter
                    if letter != word[i] and letter != '*' and self.board[x + i][y].mod_type is None:
                        raise ValueError("Невозможно вставить слово " + word)
                    elif letter == word[i]:
                        used_letters.append(letter)
                        f = True

            else:
                raise ValueError("Слово " + word + " выходит за границы по вертикали")
        else:
            if y + len(word) - 1 <= 15:
                for i in range(len(word)):
                    letter = self.board[x][y + i].cur_letter
                    if letter != word[i] and letter != '*' and self.board[x][y + i].mod_type is None:
                        raise ValueError("Невозможно вставить слово " + word)
                    elif letter == word[i]:
                        used_letters.append(letter)
                        f = True
            else:
                raise ValueError("Слово " + word + " выходит за границы по горизонтали")
        if f:
            let_of_word = list(word)  # уберем те буквы что есть на поле
            if let_of_word == used_letters:
                raise ValueError("Все буквы предложенного слова уже лежат на доске")
            else:
                for elem in used_letters:
                    let_of_word.remove(elem)

        else:
            raise ValueError("Выложенное слово не будет пересекаться с другими словами")

        #проверим, что оставшиеся буквы есть у пользователя
        if not cur_player.has_letters(let_of_word):
            raise ValueError("У " + cur_player.get_name() + " нет нужных букв")

        return let_of_word  # возвращаем буквы которые нужно удалять из руки игрока

    def set_word(self, inp, cur_player):  # вставляет слово вызывает (вызывает функцию проверки и тд) и возвращает стоимость слова
        # inp - строка, поданная на вход из консоли в формате "word x y u/h", где x и y - координаты начала слова,
        # а u/h - способ выкладки слово(вертикально или горизонтально) посмотрел на доску у своей scrabble,
        # там нумерация ячеек как в морском бое: цифры и буквы и начало координат в левом верхнем углу,
        # предлагаю сделать так же
        """Помещает слово на игровое поле"""
        deleting = self.check_word(inp, cur_player)
        word, x, let, way = inp.split()  # слово, координаты, способ выкладки
        x = int(x)
        let = let.upper()
        y = ord(let) - 1039  # так как ord('A') = 1040
        word = word.upper()
        count = 0
        modifier = 1
        if way == 'u':
            index = x
            for letter in word:
                if letter in deleting:
                    cur_player.letters.remove(letter)  #удаляем буквы из руки игрока
                cell = self.board[index][y]
                if cell.mod_type == 'word':
                    modifier *= cell.modifier
                count += cell.set_letter(letter)
                index += 1

        else:
            index = y
            for letter in word:
                if letter in deleting:
                    cur_player.letters.remove(letter)  #удаляем буквы из руки игрока
                cell = self.board[x][index]
                if cell.mod_type == 'word':
                    modifier *= cell.modifier
                count += cell.set_letter(letter)
                index += 1

        return modifier * count

