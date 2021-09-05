from __future__ import unicode_literals, absolute_import, division, print_function

import random
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
    WHITE = ColorObj('white', 'белый', ['белы', 'бела', 'бело'])
    RED = ColorObj('red', 'красный', ['красн'])
    YELLOW = ColorObj('yellow', 'жёлтый', ['желт', 'жёлт'])
    BLUE = ColorObj('blue', 'синий', ['сини', 'синя', 'сине'])
    GREEN = ColorObj('green', 'зелёный', ['зелен', 'зелён'])
    BLACK = ColorObj('black', 'чёрный', ['чёрн', 'черн'])
    ORANGE = ColorObj('orange', 'оранжевый', ['оранжев'])
    PURPLE = ColorObj('purple', 'фиолетовый', ['фиолетов'])
    PINK = ColorObj('pink', 'розовый', ['розов', 'роза'])
    GRAY = ColorObj('gray', 'серый', ['серы', 'серо', 'сера'])
    LIGHT_BLUE = ColorObj('light_blue', 'голубой', ['голуб'])
    BROWN = ColorObj('brown', 'коричневый', ['коричнев'])
    BIRUZA = ColorObj('biruza', 'бирюзовый', ['бирюз', 'берез'])


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

    def get_full_answer(self) -> AnyStr:
        """ Полный ответ на вопрос """
        text = "если смешать {} и {}, то получится {}".format(
            self.mix[0].ru,
            self.mix[1].ru,
            self.answer.ru
        )
        return text

    def get_text_question(self) -> AnyStr:
        """ Текст вопроса """
        index = random.choice((0, 1))
        index2 = 1 if index == 0 else 0
        text = "Какой цвет получится, если смешать ^{}^ и {}?".format(
            self.mix[index].ru,
            self.mix[index2].ru
        )
        return text


COLOR_MIX = [
    ColorMixObj(anwser=Color.ORANGE, mix=(Color.YELLOW, Color.RED)),
    ColorMixObj(anwser=Color.PURPLE, mix=(Color.RED, Color.BLUE)),
    ColorMixObj(anwser=Color.PINK, mix=(Color.RED, Color.WHITE)),
    ColorMixObj(anwser=Color.GRAY, mix=(Color.WHITE, Color.BLACK)),
    ColorMixObj(anwser=Color.GREEN, mix=(Color.YELLOW, Color.BLUE)),
    ColorMixObj(anwser=Color.LIGHT_BLUE, mix=(Color.BLUE, Color.WHITE)),
    ColorMixObj(anwser=Color.BROWN, mix=(Color.GREEN, Color.RED)),
    ColorMixObj(anwser=Color.BROWN, mix=(Color.BLACK, Color.YELLOW)),
    ColorMixObj(anwser=Color.BIRUZA, mix=(Color.GREEN, Color.BLUE)),
    ColorMixObj(anwser=Color.BLUE, mix=(Color.LIGHT_BLUE, Color.PURPLE)),
]
