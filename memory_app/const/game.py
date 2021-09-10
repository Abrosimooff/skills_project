
class Game:
    name = None
    name_ru = None
    checked_names = []

    def __init__(self, name, name_ru, checked_names) -> None:
        self.name = name
        self.name_ru = name_ru
        self.checked_names = checked_names


class Games:
    JUST_GAME = Game('just_game', 'запоминай слова', ['слова'])
    REVERSE_GAME = Game('reverse_game', 'игра наоборот', ['наоборот'])
    TEXT_REPETITION_GAME = Game('text_repetition_game', 'запоминай рассказ', ['рассказ'])

    @classmethod
    def get_game_list(cls):
        return [
            cls.JUST_GAME,
            # cls.REVERSE_GAME,
            cls.TEXT_REPETITION_GAME
        ]


WORD_RU = {
    0: 'слов',
    1: 'слово',
    2: 'слова',
    3: 'слова',
    4: 'слова',
    5: 'слов',
    6: 'слов',
    7: 'слов',
    8: 'слов',
}


NEXT_ROUND_HELP = 'Чтобы перейти к следующему раунду — скажите "следующий раунд" или "пропусти раунд"!'

NEXT_ROUND_WORDS = [
    'следующий раунд',
    'пропусти раунд',
    'пропустить раунд',
    'сдаюсь',
]