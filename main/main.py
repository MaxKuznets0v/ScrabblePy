"""Главный игровой файл"""
from resources import *
# from resources.gameboard import GameBoard
import random
# from resources.cell import Cell
# from resources.player import Player
from resources import Utils


class Scrabble:
    """Основной игровой класс"""
    def _set_bag(self):
        """Инициализация таблицы количества букв"""
        self._let_to_amount = Utils.bag
        self._amount_of_letters = Utils.amount_of_letters

    def _create_players(self):
        """Создает 2 игроков"""
        name1 = input("Введите имя первого игрока: ")
        name2 = input("Введите имя второго игрока: ")
        self.player_list = [Player(0, name1, self._let_to_amount, self._amount_of_letters),
                            Player(0, name2, self._let_to_amount, self._amount_of_letters)]
        self.turn = random.randint(0, len(self.player_list) - 1)  # текущий ход игрока turn - индекс игрока в списке

    def _next_turn(self):
        """Передает ход следующему игроку"""
        self.turn = (self.turn + 1) % len(self.player_list)

    def _make_turn(self):
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
                self.player_list[self.turn].score += self.set_word(inp)
                if self._amount_of_letters > 0:  # если в мешочке есть буквы, то выдадим их игроку и запомним новое число букв в мешочке
                    self._amount_of_letters = self.player_list[self.turn].take_letters(self._let_to_amount, self._amount_of_letters)
                self._next_turn()
                break
            except TypeError as er:
                print(er)
            except ValueError as er:
                print(er)
            except Exception:
                print("Что-то пошло не так")

    def _set_dict(self):
        """Получение словаря возможных слов"""
        f = open(Utils.dict, encoding="utf-8")
        self._dict = set(f.read().split(','))
        f.close()

    def __init__(self):
        self.board = GameBoard()
        self._set_bag()
        self._create_players()
        self._set_dict()
        self.main()

    def show_rules(self):  # TODO: правила
        print("Правила:")
        print("Здесь можно расписать правила")
        print("Каждый ход совершается в следующем формате(без кавычек):\n'слово число(1-15) буквы(А-О) режим вставки(u/h)'")
        print("Здесь u - вертикальная вставка сверху вниз, h - гороизонтальная справа налево, буквы А-О, без Ё")

    def check_word(self, inp):  # TODO: параллельный ввод
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
        if x.isdigit() and y in list(Utils.y_axis):
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
                    letter = self.board.board[x + i][y].cur_letter
                    if letter != word[i] and letter != Utils.gap_filler and self.board.board[x + i][y].mod_type is None:
                        raise ValueError("Невозможно вставить слово " + word)
                    elif letter == word[i]:
                        used_letters.append(letter)
                        f = True

            else:
                raise ValueError("Слово " + word + " выходит за границы по вертикали")
        else:
            if y + len(word) - 1 <= 15:
                for i in range(len(word)):
                    letter = self.board.board[x][y + i].cur_letter
                    if letter != word[i] and letter != Utils.gap_filler and self.board.board[x][y + i].mod_type is None:
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
        if not self.player_list[self.turn].has_letters(let_of_word):
            raise ValueError("У " + self.player_list[self.turn].name() + " нет нужных букв")

        return let_of_word  # возвращаем буквы которые нужно удалять из руки игрока

    def set_word(self, inp):  # вставляет слово вызывает (вызывает функцию проверки и тд) и возвращает стоимость слова
        # inp - строка, поданная на вход из консоли в формате "word x y u/h", где x и y - координаты начала слова,
        # а u/h - способ выкладки слово(вертикально или горизонтально) посмотрел на доску у своей scrabble,
        # там нумерация ячеек как в морском бое: цифры и буквы и начало координат в левом верхнем углу,
        # предлагаю сделать так же
        """Помещает слово на игровое поле"""
        deleting = self.check_word(inp)
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
                    self.player_list[self.turn].letters.remove(letter)  #удаляем буквы из руки игрока
                cell = self.board.board[index][y]
                if cell.mod_type == 'word':
                    modifier *= cell.modifier
                count += cell.set_letter(letter)
                index += 1

        else:
            index = y
            for letter in word:
                if letter in deleting:
                    self.player_list[self.turn].letters.remove(letter)  #удаляем буквы из руки игрока
                cell = self.board.board[x][index]
                if cell.mod_type == 'word':
                    modifier *= cell.modifier
                count += cell.set_letter(letter)
                index += 1

        return modifier * count

    def main(self):  # TODO: критерий остановки
        playing = True
        self.show_rules()
        while playing:
            self.board.print_board()
            print("Ход игрока", self.player_list[self.turn].name)
            print("Буквы " + self.player_list[self.turn].name + ":")
            print(*self.player_list[self.turn].letters, sep=Utils.let_sep)
            self._make_turn()
        # По окончанию игры сравнить баллы и вывести на экран имя победителя

game = Scrabble()