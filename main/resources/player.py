class Player:
    """Класс игрока с полями score и user_name"""
    def __init__(self, score, name):
        self.score = score
        self._user_name = name

    def get_name(self):
        return self._user_name
