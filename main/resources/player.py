import random
from resources import Utils


class Player:
    """Класс игрока с полями score, user_name, letters и passes - кол-во пропусков подряд"""

    def __init__(self, score, name):
        self.score = score
        self._name = name
        self.letters = list()
        self.passes = 0

    @property
    def name(self):
        """Возвращает имя игрока"""
        return self._name

    def has_letters(self, letters):
        """Проверяет, есть ли необходимые буквы у игрока"""
        user_let = list(self.letters)  # копируем список букв
        given_let = list(letters)
        needed_letters = list()  # список, нужный для букв, заменяемых пустышками
        empty = user_let.count(' ')  # подсчет количества пустышек
        length = len(given_let)  # запомним количество букв в изначальном слове
        let_count = 0
        for i in range(length):
            ch = given_let.pop()
            if ch in user_let:
                user_let.remove(ch)
                let_count += 1  # выкидываем по одной из скопированных букв пользователя и увеличиваем счетчик
            else:
                needed_letters.append(ch)  # сохраним для случая, если не хватит 1 буквы

        if empty != 0 and empty == length - let_count:  # если разница имеющихся букв и количетсво пустышек равны спросим,
            # использовать ли их, иначе вернем False
            ans = "э"
            while ans != "да" and ans != "нет":
                if empty == 1:
                    ans = input(f"Вам не хватает {empty} буквы, хотите использовать пустую фишку?(да/нет)")
                else:
                    ans = input(f"Вам не хватает {empty} букв, хотите использовать пустые фишки?(да/нет)")
                ans = ans.lower()

            if ans == "нет":
                return False
            else:
                for letter in needed_letters:
                    self.letters.remove(' ')
                    self.letters.append(letter)  # удалим пустышку и добавим нужную букву
        elif length != let_count:
            return False

        return True
