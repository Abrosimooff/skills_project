from __future__ import unicode_literals, absolute_import, division, print_function

from typing import Dict

from memory_app.states.base import MemoryGameStateBase


class JustGameState(MemoryGameStateBase):
    """ Простая игра. Состояние """
    words = None                # Заданные в этом раунде слова
    answered_words = None       # Отвеченые в этом раунде слова
    try_count = None            # Номер попытки текущего раунда
    scores = None               # Баллы в этой сессии (игре)
    category = None             # Выбранная категория в этой игре
    action = None               # куда пойдёт следующий запрос

    WORDS_ROUNDS = range(3, 8)  # Количество слов раундах
    MAX_TRY_COUNT = 3

    def __init__(self, state: Dict) -> None:
        self.words = state.get('words', [])
        self.answered_words = state.get('answered_words', [])
        self.try_count = state.get('try_count', 0)
        self.scores = state.get('scores', 0)
        self.category = state.get('category')
        self.action = state.get('action')

        if not state:
            self.action = 'just_game_category_select'  # todo router

    def serialize(self) -> Dict:
        return dict(
            category=self.category,
            words=self.words,
            answered_words=self.answered_words,
            try_count=self.try_count,
            scores=self.scores,
            action=self.action
        )
