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
