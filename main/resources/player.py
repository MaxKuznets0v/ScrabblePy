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

    def take_letters(self, bag):
        """Берем буквы из мешочка"""
        while len(self.letters) < 7:
            cur_letter = random.choice(list(bag.keys()))
            if bag[cur_letter] > 0:
                bag[cur_letter] -= 1
                self.letters.append(cur_letter)
            continue

    def has_letters(self, letters):
        """Проверяет, есть ли необходимые буквы у игрока"""
        user_let = list(self.letters)  #копируем список букв
        given_let = list(letters)
        for i in range(len(given_let)):
            ch = given_let.pop().upper()
            try:
                user_let.remove(ch)
            except ValueError:
                return False
        return True
