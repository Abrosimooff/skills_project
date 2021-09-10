from __future__ import unicode_literals, absolute_import, division, print_function

from typing import AnyStr


def tts_to_text(tts: AnyStr) -> AnyStr :
    """ убираем `^ <speaker> из текста  """
    LETTERS = ('`', '^')
    SPEAKER_START = '<speaker'
    SPEAKER_END = '>'

    text = tts
    for letter in LETTERS:
        text = text.replace(letter, '')

    while SPEAKER_START in text:
        start = text.index(SPEAKER_START)
        end = text.index(SPEAKER_END)
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
