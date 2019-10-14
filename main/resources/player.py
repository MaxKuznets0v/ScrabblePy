class Player:
    """Класс игрока с полями score, user_name и letters"""

    def __init__(self, score, name, letters):
        self.score = score
        self._user_name = name
        self.letters = letters

    def get_name(self):
        """Возвращает имя игрока"""
        return self._user_name

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
