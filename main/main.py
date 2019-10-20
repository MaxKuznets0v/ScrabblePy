"""Главный игровой файл"""
from resources import *
import random
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
        self.player_list = [Player(0, name1),
                            Player(0, name2)]
        for pl in self.player_list:
            self.take_letters(pl)
        self.turn = random.randint(0, len(self.player_list) - 1)  # текущий ход игрока turn - индекс игрока в списке

    def _next_turn(self):
        """Передает ход следующему игроку"""
        self.turn = (self.turn + 1) % len(self.player_list)

    def _make_turn(self):
        """Совершает ход, защитывает очки и переводит ход"""
        while True:
            try:
                inp = input("Ваш ход:")
                inp_expr = list(inp.split())
                if inp.lower() == "правила":  # выводит правила по необходимости
                    self.show_rules()
                    continue
                elif inp_expr[0].lower() == "пас":  # пропуск хода
                    if len(inp_expr) > 1:  # если ввели пас и далее буквы, то заменяем эти буквы
                        self.exchange(inp_expr[1:])  # передадим все буквы кроме слова пас
                    self.player_list[self.turn].passes += 1  # увеличиваем счетчик пропусков
                    self._next_turn()
                    break
                self.player_list[self.turn].score += self.set_word(inp)
                self.take_letters(self.player_list[self.turn])
                for pl in self.player_list:
                    pl.passes = 0  # обнуляем пропуски после хода
                #  self.player_list[self.turn].passes = 0
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

    def _score(self, player):
        """Требуется как ключ для сортировки"""
        return player.score

    def __init__(self):
        self.board = GameBoard()
        self._set_bag()
        self._create_players()
        self._set_dict()
        self.main()

    def exchange(self, ex_let):
        """Принимает буквы, которые нужно сбросить и сбрасывает их"""
        if len(ex_let) <= Utils.n_player_let:  # этот блок проверяет, что нужные буквы есть у игрока
            user_let = list(self.player_list[self.turn].letters)  # копируем список букв игрока
            given_let = list(ex_let)  # скопируем введенные буквы
            for i in range(len(given_let)):
                ch = given_let.pop().upper()
                if ch == '_':  # так как пустышку обозначили за _
                    ch = ' '
                    ex_let.remove('_')
                    ex_let.append(' ')  # заменим '_' на ' ' так как у игрока опустышка индексируется так
                try:
                    user_let.remove(ch)
                except ValueError:  # бросится исключение, если в user_let нет данной буквы
                    raise ValueError("У вас нет нужных букв!")  # ловим и пробрасываем новое исключение

            for letter in ex_let:  # этот блок занимается удалением буквы из руки и выдачей новых
                self._let_to_amount[letter] += 1
                self._amount_of_letters += 1
                self.player_list[self.turn].letters.remove(letter)

            self.take_letters(self.player_list[self.turn])
        else:
            raise ValueError("У вас нет столько букв!")

    def take_letters(self, player):
        """Берем буквы из мешочка"""
        while len(player.letters) < Utils.n_player_let and self._amount_of_letters != 0:
            cur_letter = random.choice(list(self._let_to_amount.keys()))
            if self._let_to_amount[cur_letter] > 0:
                self._let_to_amount[cur_letter] -= 1
                self._amount_of_letters -= 1
                player.letters.append(cur_letter)
            continue

    def game_over(self):
        """Проверка на окончание игры
        Если игроки два раза подряд пасанут игра заканчивается"""
        for pl in self.player_list:
            if pl.passes != Utils.max_passes:  # Если все игроки имеют максимальное коло-во пасов, сюда не зайдет
                return False
        return True

    def show_rules(self):  # TODO: правила
        print("Правила:")
        print("Здесь можно расписать правила")
        print("Каждый ход совершается в следующем формате(без кавычек):\n'слово число(1-15) буквы(А-О) режим вставки(в/г)'")
        print("Здесь в - вертикальная вставка сверху вниз, г - гороизонтальная справа налево, буквы А-О, без Ё")
        print("Для пропуска хода введите: 'пас' и далее через пробел, отбрасывемые буквы(для пропуска хода без сброса букв")
        print("пишите 'пас' без последующих букв), пустышка обозначается '_'")

    def check_word(self, inp):  # TODO: параллельный ввод
        # проверяет на формат: (слово, x, буква, способ выкладки) пример: "сосна 11 О u" иначе бросить исключение
        # TypeError само слово на корректность (есть ли слово в словаре, не выезжает ли оно за границы,
        # есть ли нужные буквы для этого слова у пользователя, пересекает ли оно необходимые буквы и тд,
        # иначе бросаем ValueError
        """Проверка ввода пользователя на корректность"""
        # проверим, что на вход получили 4 значения
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
        else:
            raise TypeError(str(x) + " не число или " + str(y) + " не буква")

        # проверим что последний параметр u/h
        way = way.lower()
        if way != Utils.hor_dir and way != Utils.vert_dir:
            raise TypeError("Выбрано неверное направление(г/в)")

        # проверим, что слово есть в словаре
        if word.lower() not in self._dict:
            raise ValueError("Слова " + word.upper() + " нет в словаре")
        word = word.upper()
        # проверим, что слово не выходит за край, если выполнено проверяем остальное
        used_letters = list()  # у игрока могут быть не все необходимые буквы, главное, чтобы они лежали на поле
        has_intersec = False  # флаг, отвечающий за проверку того, что хотя бы раз было пересечено уже выложенное на доске слово
        if way == Utils.vert_dir:
            if x + len(word) < 15:
                for i in range(len(word)):
                    letter = self.board.board[x + i][y].cur_letter
                    if letter != word[i] and letter != Utils.gap_filler and self.board.board[x + i][y].mod_type is None:
                        raise ValueError("Невозможно вставить слово " + word)
                    elif letter == word[i]:
                        used_letters.append(letter)
                        has_intersec = True

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
                        has_intersec = True
            else:
                raise ValueError("Слово " + word + " выходит за границы по горизонтали")
        if True:
            let_of_word = list(word)  # уберем те буквы что есть на поле
            if let_of_word == used_letters:
                raise ValueError("Все буквы предложенного слова уже лежат на доске")
            else:
                for elem in used_letters:
                    let_of_word.remove(elem)

        else:
            raise ValueError("Выложенное слово не будет пересекаться с другими словами")

        # проверим, что оставшиеся буквы есть у пользователя
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
        if way == Utils.vert_dir:
            index = x
            for letter in word:
                if letter in deleting:
                    self.player_list[self.turn].letters.remove(letter)  # удаляем буквы из руки игрока
                cell = self.board.board[index][y]
                if cell.mod_type == 'word':
                    modifier *= cell.modifier
                    cell.make_none()
                count += cell.set_letter(letter)
                index += 1

        else:
            index = y
            for letter in word:
                if letter in deleting:
                    self.player_list[self.turn].letters.remove(letter)  # удаляем буквы из руки игрока
                cell = self.board.board[x][index]
                if cell.mod_type == 'word':
                    modifier *= cell.modifier
                    cell.make_none()
                count += cell.set_letter(letter)
                index += 1

        return modifier * count

    def main(self):
        playing = True
        self.show_rules()
        while playing:
            self.board.print_board()
            print("Ход игрока", self.player_list[self.turn].name)
            print("Буквы " + self.player_list[self.turn].name + ":")
            print(*self.player_list[self.turn].letters, sep=Utils.let_sep)
            # выведем стоимость буквы под ними
            for i in range(len(self.player_list[self.turn].letters)):
                if i != len(self.player_list[self.turn].letters) - 1:
                    print(Utils.let_to_price[self.player_list[self.turn].letters[i]], end=Utils.let_sep)
                else:
                    print(Utils.let_to_price[self.player_list[self.turn].letters[i]])

            self._make_turn()
            if self.game_over():
                playing = False

        print("\n")
        self.player_list.sort(key=self._score, reverse=True)
        max_score = self.player_list[0].score
        eq_score = 0
        for pl in self.player_list:  # если несколько игроков имеет одинаковые очки
            if pl.score == max_score:
                eq_score += 1

        if eq_score > 1:
            print("НИЧЬЯ!")
            print("Победили: ", end="")  # выводим имена игроков - победителей
            for i in range(eq_score):
                print(self.player_list[i].name, end=", ")
        else:
            print("ПОБЕДА ", self.player_list[0].name)

        print("Количество очков победителя:", self.player_list[0].score)
        for i in range(eq_score, len(self.player_list)):
            print(self.player_list[i].name, ':', self.player_list[i].score)

game = Scrabble()
