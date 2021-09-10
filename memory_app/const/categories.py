from __future__ import unicode_literals, absolute_import, division, print_function

from typing import List


class Category:
    name = None
    check_names = []
    words = []

    def __init__(self, name, check_names, words) -> None:
        self.name = name
        self.check_names = check_names
        self.words = words


class W:
    """ Слово """
    name = None
    check_names = []

    def __init__(self, name, check_names: List = None) -> None:
        self.name = name
        self.check_names = [name]
        if check_names:
            self.check_names.extend(check_names)

# todo уникальность


HOME = Category('дом', ['дом'], words=["стол", "стул", "кровать", "картина", "кухня", "книга", "телефон", "часы",
                                       "окно", "шкаф", "диван", "щётка", "бумага", "банка", "коробка", "лампа",
                                       "будильник", "подушка", "одеяло", "ложка"])
NATURE = Category('природа', ['природ'], words=["трава", "куст", "дерево", "дорога", "скала", "река", "море",
                                                "ветер", "солнце", "дождь", "цветок", "закат", "камень", "остров" ])
FOOD = Category('еда', ['еда'], words=["сыр", "колбаса", "хлеб", "молоко", "каша", "суп", "мясо", "рыба", "вода",
                                       "картошка", "огурец", "помидор", "масло", "апельсин", "лук", "яблоко",
                                       "компот", "сок", "гречка", "рис", "блин", "салат"])

ALL = Category('все', ['все', 'всё'], words=HOME.words + NATURE.words + FOOD.words)

CATEGORIES = (
    HOME,
    NATURE,
    FOOD,
    ALL
)
