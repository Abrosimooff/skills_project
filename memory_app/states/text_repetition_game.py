from __future__ import unicode_literals, absolute_import, division, print_function

from typing import Dict

from memory_app.states.base import MemoryGameStateBase


class TextRepetitionGameState(MemoryGameStateBase):
    """ Игра изложение - Пишем несложный текст, предложение за предложением, проверяем точность ответа от пользователя
        Состояние
    """
    text_id = None      # какой текст пишем
    text_line = None    # какое предложение
    scores = None       # список [сколько процентов совпадения в каждом предложении]
    action = None

    def __init__(self, state: Dict) -> None:
        self.text_id = state.get('text_id')
        self.text_line = state.get('text_line')
        self.scores = state.get('scores', [])
        self.action = state.get('action')

        if not state:
            self.action = 'text_repetition_game_process'

    def serialize(self) -> Dict:
        return dict(
            text_id=self.text_id,
            text_line=self.text_line,
            scores=self.scores,
            action=self.action
        )
