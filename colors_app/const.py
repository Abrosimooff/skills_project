from __future__ import unicode_literals, absolute_import, division, print_function

from typing import Tuple, AnyStr


class ColorObj(object):
    id = None
    ru = None
    mrc_ru = None
    answers = []

    def __init__(self, id, ru, answers=None, mrc_ru=None) -> None:
        self.id = id
        self.ru = ru
        self.answers = answers  # Возможные варианты ответа


class Color(object):
    WHITE = ColorObj('white', 'Белый', ['белы', 'бела', 'бело'])
    RED = ColorObj('red', 'Красный', ['красн'])
    YELLOW = ColorObj('yellow', 'Жёлтый', ['желт', 'жёлт'])
    BLUE = ColorObj('blue', 'Синий', ['сини', 'синя', 'сине'])
    GREEN = ColorObj('green', 'Зелёный', ['зелен', 'зелён'])
    BLACK = ColorObj('black', 'Чёрный', ['чёрн', 'черн'])
    ORANGE = ColorObj('orange', 'Оранжевый', ['оранжев'])
    PURPLE = ColorObj('purple', 'Фиолетовый', ['фиолетов'])
    PINK = ColorObj('pink', 'Розовый', ['розов', 'роза'])
    GRAY = ColorObj('gray', 'Серый', ['серы', 'серо', 'сера'])
    LIGHT_BLUE = ColorObj('light_blue', 'Голубой', ['голуб'])
    BROWN = ColorObj('brown', 'Коричневый', ['коричнев'])


class ColorMixObj(object):
    answer = None
    mix = None

    def __init__(self, anwser: ColorObj, mix: Tuple[ColorObj, ColorObj]) -> None:
        self.answer = anwser
        self.mix = mix

    def user_answer_is_valid(self, user_answer: AnyStr):
        """ Верный ли ответ пользователя """
        for variant in self.answer.answers:
            if variant.lower() in user_answer.lower():
                return True
        return False


COLOR_MIX = [
    ColorMixObj(anwser=Color.ORANGE, mix=(Color.YELLOW, Color.RED)),
    ColorMixObj(anwser=Color.PURPLE, mix=(Color.RED, Color.BLUE)),
    ColorMixObj(anwser=Color.PINK, mix=(Color.RED, Color.WHITE)),
    ColorMixObj(anwser=Color.GRAY, mix=(Color.WHITE, Color.BLACK)),
    ColorMixObj(anwser=Color.GREEN, mix=(Color.YELLOW, Color.BLUE)),
    ColorMixObj(anwser=Color.LIGHT_BLUE, mix=(Color.BLUE, Color.WHITE)),
    ColorMixObj(anwser=Color.BROWN, mix=(Color.GREEN, Color.RED)),
]
