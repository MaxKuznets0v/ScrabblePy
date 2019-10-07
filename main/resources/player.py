#from resources.scrabble import Scrabble


class Player:
    """Класс игрока с полями score, user_name и letters"""

    def __init__(self, score, name, letters):
        self.score = score
        self._user_name = name
        self.letters = letters

    def get_name(self):
        return self._user_name
