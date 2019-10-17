import random
from resources import Utils


class Player:
    """Класс игрока с полями score, user_name и letters"""

    def __init__(self, score, name):
        self.score = score
        self._name = name
        self.letters = list()

    @property
    def name(self):
        """Возвращает имя игрока"""
        return self._name

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
