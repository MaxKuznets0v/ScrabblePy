import random


class Player:
    """Класс игрока с полями score, user_name и letters"""

    def _init_letters(self, bag):
        """Выставляет буквы игроков при старте"""
        self.letters = list()
        self.take_letters(bag)

    def __init__(self, score, name, bag):
        self.score = score
        self._user_name = name
        self._init_letters(bag)

    def get_name(self):
        """Возвращает имя игрока"""
        return self._user_name

    def take_letters(self, bag, am_of_let=103):
        """Берем буквы из мешочка"""
        count = am_of_let  # счетчик числа букв в мешочке
        while len(self.letters) < 7 and count != 0:
            cur_letter = random.choice(list(bag.keys()))
            if bag[cur_letter] > 0:
                bag[cur_letter] -= 1
                count -= 1
                self.letters.append(cur_letter)
            continue
        return count

    def has_letters(self, letters):
        """Проверяет, есть ли необходимые буквы у игрока"""
        user_let = list(self.letters)  # копируем список букв
        given_let = list(letters)
        has_empty = ' ' in user_let
        length = len(given_let)  # запомним количество букв в изначальном слове
        let_count = 0
        for i in range(length):
            ch = given_let.pop()
            if ch in user_let:
                user_let.remove(ch)
                let_count += 1  # выкидываем по одной из скопированных букв пользователя и увеличиваем счетчик
            else:
                needed_letter = ch  # сохраним для случая, если не хватит 1 буквы

        if has_empty and length - let_count == 1:  # если разница в 1 букву и пользователя есть пустая ячейка спросим,
            # использовать ли ее, иначе вернем False
            ans = "э"
            while ans != "да" and ans != "нет":
                ans = input("Вам не хватает 1 буквы, хотите использовать пустую фишку?(да/нет)")
                ans = ans.lower()

            if ans == "нет":
                return False
            else:
                self.letters.remove(' ')
                self.letters.append(needed_letter)  # удалим пустышку и добавим нужную букву
        elif length != let_count:
            return False

        return True
