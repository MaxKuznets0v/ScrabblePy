from resources import Utils


class Cell:
    """Ячейка игрового поля"""

    def __init__(self, type_=None, letter=Utils.gap_filler, mod=1):
        # желательно проверять, что ввелась именно строка длиной 1 и это буква
        self.let_to_price = Utils.let_to_price
        self.cur_letter = letter
        self.modifier = mod
        self.mod_type = type_

    def make_none(self):
        """Очищает модификатор ячейки"""
        self.modifier = 1
        self.mod_type = None

    def set_letter(self, letter):  # изменяет букву в ячейке и возвращает количество очков за эту букву
        """Помещает букву в ячейку"""
        self.cur_letter = letter[0]  # берем первый элемент буквы(может быть больше одного элемента из-за пустышки)
        if len(letter) > 1:  # длина буквы будет больше 1 если была метка '-'
            res = self.let_to_price[' ']
        else:
            res = self.let_to_price[letter]
        if self.mod_type == "letter":
            res *= self.modifier
            self.make_none()
        return res
