from typing import AnyStr, Optional


class Game:
    name = None
    name_ru = None
    checked_names = []

    def __init__(self, name, name_ru, checked_names) -> None:
        self.name = name
        self.name_ru = name_ru
        self.checked_names = checked_names


class Games:
    JUST_GAME = Game('just_game', 'запоминай слова', ['слова', 'перв'])
    TEXT_REPETITION_GAME = Game('text_repetition_game', 'запоминай рассказ', ['рассказ', 'втор'])
    REVERSE_GAME = Game('reverse_game', 'игра наоборот', ['наоборот'])

    @classmethod
    def get_game_list(cls):
        return [
            cls.JUST_GAME,
            cls.TEXT_REPETITION_GAME,
            # cls.REVERSE_GAME,
        ]

    @classmethod
    def get_game_by_name(cls, name: AnyStr) -> Optional[Game]:
        GAME_MAP = {game.name: game for game in cls.get_game_list()}
        return GAME_MAP.get(name)


WORD_RU = {
    0: 'ноль слов',
    1: 'одно слово',
    2: 'два с`лова',
    3: 'три с`лова',
    4: 'четыре с`лова',
    5: 'пять слов',
    6: 'шесть слов',
    7: 'семь слов',
    8: 'восемь слов',
}


NEXT_ROUND_SUPER_PHRASES = [
    'Супер! Все слова этого раунда засчитаны.',
    'Поздравляю, это был успешный раунд!',
    'Отличный раунд, я засчитала все слова.',
    'С этим раундом Вы справились на отлично!'
]
NEXT_ROUND_WORD_COUNT = [
    'В этом раунде вы запомнили',
    'В этом раунде я засчитала',
    'За этот раунд засчитано',
    'За этот раунд угадано',
    'Готово! В этом раунде засчитано',
]

NEXT_ROUND_HELP = 'Чтобы перейти к следующему раунду — скажите "следующий раунд" или "пропусти раунд"!'

NEXT_ROUND_WORDS = [
    'следующий раунд',
    'пропусти раунд',
    'пропустить раунд',
    'сдаюсь',
]