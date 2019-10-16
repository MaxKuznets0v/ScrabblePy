class Cell:
    """Ячейка игрового поля"""
    def __init__(self, type_=None, letter='--', mod=1):
        # желательно проверять, что ввелась именно строка длиной 1 и это буква
        self.let_to_price = {'А': 1, 'Б': 3, 'В': 1,
                             'Г': 3, 'Д': 2, 'Е': 1,
                             'Ё': 3, 'Ж': 5, 'З': 5,
                             'И': 1, 'Й': 4, 'К': 2,
                             'Л': 2, 'М': 2, 'Н': 1,
                             'О': 1, 'П': 2, 'Р': 1,
                             'С': 1, 'Т': 1, 'У': 2,
                             'Ф': 10, 'Х': 5, 'Ц': 5,
                             'Ш': 8, 'Щ': 10, 'Ъ': 10,
                             'Ы': 4, 'Ь': 3, 'Э': 8,
                             'Ю': 8, 'Я': 3, ' ': 0}

        self.cur_letter = letter
        self.modifier = mod
        self.mod_type = type_

    def make_none(self):
        """Очищает модификатор ячейки"""
        self.modifier = 1
        self.mod_type = None

    def set_letter(self, letter):  # изменяет букву в ячейке и возвращает количество очков за эту букву
        """Помещает букву в ячейку"""
        self.cur_letter = letter
        res = self.let_to_price[letter]
        if self.mod_type == "letter":
            res *= self.modifier
        self.make_none()
        return res
