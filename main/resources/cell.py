class Cell:
    """Ячейка игрового поля"""
    def __init__(self, type_=None, letter='*', mod=1):
        self.cur_letter = letter # желательно проверять, что ввелась именно строка длиной 1 и это буква
        self.modifier = mod
        self.mod_type = type_

    def set_letter(self, letter):  # изменяет букву в ячейке и возвращает количество очков за эту букву
        pass
