from __future__ import unicode_literals, absolute_import, division, print_function

import re
from typing import AnyStr

from django.utils.functional import classproperty
from core.utils.misc import SafeContext


def tts_to_text(tts: AnyStr) -> AnyStr :
    """ убираем `^ <speaker> из текста  """
    LETTERS = ('`', '^')

    SPEAKER_START = '<speaker'
    SPEAKER_END = '>'

    EMOJI_START = '&#'
    EMOJI_END = ';'

    text = tts
    for letter in LETTERS:
        text = text.replace(letter, '')

    while SPEAKER_START in text:
        start = text.index(SPEAKER_START)
        end = text.index(SPEAKER_END)
        text = text[:start] + text[end + 1:]

    while EMOJI_START in text:
        start = text.index(EMOJI_START)
        end = text.index(EMOJI_END)
        text = text[:start] + text[end + 1:]

    return text


def clean_text(text: AnyStr) -> AnyStr:
    """ Текст привести к общему простому виду """
    text = text.lower()
    text = text.replace("ё", "е")
    return text


def clean_punctuation(text: AnyStr) -> AnyStr:
    """ убрать пунктуацию из текста """
    text = text.lower()
    text = text.replace("ё", "е")
    import string
    for c in string.punctuation:
        text = text.replace(c, "")
    return text


def get_score_text(score_count):
    """ Верное склонение  сколько баллов """
    def check(digit):
        if digit in (2, 3, 4):
            return 'балла'
        if digit == 1:
            return 'балл'
        return 'баллов'

    if score_count <= 20:
        text = check(score_count)
    else:
        last_digit = int(str(score_count)[-1])
        text = check(last_digit)
    return text


def audio(audio=None, audio_vk_id=None):
    """ Получить код аудио дял вствки в tts """
    if audio:
        return '<speaker audio={}>'.format(audio)
    if audio_vk_id:
        return '<speaker audio_vk_id={}>'.format(audio_vk_id)


class AgeDetector:
    """ Определятель ВОЗРАСТА!!!  цифр (от 0 до 99) в строке """
    D0 = 'нол'
    D1 = 'один'
    D2 = 'два'
    D3 = 'три'
    D4 = 'четыр'
    D5 = 'пят'
    D6 = 'шест'
    D7 = 'сем'
    D8 = 'восем'
    D9 = 'девят'
    D10 = 'десят'

    D11 = 'одиннадцат'
    D12 = 'двенадцат'
    D13 = 'тринадцат'
    D14 = 'четырнадцат'
    D15 = 'пятнадцат'
    D16 = 'шестнадцат'
    D17 = 'семнадцат'
    D18 = 'восемнадцат'
    D19 = 'девятнадцат'

    D20 = 'двадцат'
    D30 = 'тридцат'
    D40 = 'сорок'
    D50 = 'пятьдесят'
    D60 = 'шестдесят'
    D70 = 'семдесят'
    D80 = 'восемдесят'
    D90 = 'девяносто'

    MOD1 = [D11, D12, D13, D14, D15, D16, D17, D18, D19]
    MOD10 = [D20, D30, D40, D50, D60, D70, D80, D90]

    MAP = {
        D0: 0,
        D1: 1,
        D2: 2,
        D3: 3,
        D4: 4,
        D5: 5,
        D6: 6,
        D7: 7,
        D8: 8,
        D9: 9,
        D10: 10,

        D11: 11,
        D12: 12,
        D13: 13,
        D14: 14,
        D15: 15,
        D16: 16,
        D17: 17,
        D18: 18,
        D19: 19,

        D20: 20,
        D30: 30,
        D40: 40,
        D50: 50,
        D60: 60,
        D70: 70,
        D80: 80,
        D90: 90,
    }

    @classproperty
    def mod1_values(cls):
        return [cls.MAP[x] for x in cls.MOD1]

    @classproperty
    def mod10_values(cls):
        return [cls.MAP[x] for x in cls.MOD10]

    @classmethod
    def detect(cls, text: AnyStr) -> int:

        text = clean_text(text)

        # Если в текте прям ЦИФРЫ - то по ним определяем
        digit_list = re.findall('\d+', text)
        if digit_list and int(digit_list[0]) < 100:
            return int(digit_list[0])

        # Иначе по текстовым числительным
        digits = []

        # Собираем все совпадения по цифрам
        for key, value in cls.MAP.items():  # Ходим по каждой цифре от 0 до 9
            matches = [SafeContext(value=value, index=item.start()) for item in re.finditer(key, text)]
            digits.extend(matches)

        mod1_in_digits = any(filter(lambda x: x.value in cls.mod1_values, digits))  # в списке есть 11 - 19
        mod10_in_digits = any(filter(lambda x: x.value in cls.mod10_values, digits))  # в списке есть 20, 30, 40...90
        exists8 = any(filter(lambda x: x.value == 8, digits))
        exists18 = any(filter(lambda x: x.value == 18, digits))
        exists80 = any(filter(lambda x: x.value == 80, digits))

        # исклчюаем из matches такие случаи как:
        # тринадцать = [3, 13]
        # шестдесят = [10, 60]
        # восемь = [7, 8]
        # восемнадцать = [7, 8]
        def filter_fn(x):
            result = False
            if mod1_in_digits:
                result = x.value in cls.mod1_values
                if exists18:
                    result = result and x.value != 17
                return result

            elif mod10_in_digits:
                result = x.value != cls.MAP[cls.D10] and (
                        (x.value in cls.mod10_values) or
                        (x.value not in cls.mod1_values and x.value not in cls.mod10_values and x.index > 0)
                )
                if exists8:
                    result = result and x.value != 7
                if exists80:
                    result = result and x.value != 70
                return result

            elif exists8:
                return x.value != 7

            return x.index == 0

        result_digits = list(filter(filter_fn, digits))

        if len(result_digits) == 1:
            return result_digits[0].value

        if len(result_digits) > 1:
            return sum(map(lambda x: x.value, result_digits))
