from __future__ import unicode_literals, absolute_import, division, print_function

from typing import Dict, AnyStr

from memory_app.const.game import Games
from memory_app.states.just_game import JustGameState
from memory_app.states.reverse_game import ReverseGameState
from memory_app.states.text_repetition_game import TextRepetitionGameState


GAME_STATE_CLASSES = {
    Games.JUST_GAME.name: JustGameState,
    Games.REVERSE_GAME.name: ReverseGameState,
    Games.TEXT_REPETITION_GAME.name: TextRepetitionGameState,
}


def get_game_state_class(game_name):
    """ Получить класс состояния игры, по названию игры """
    return GAME_STATE_CLASSES.get(game_name)


class MemoryGameGeneralState:
    """ Главный стейт скилла, который управляет играми внутри скилла """
    game_name = None
    game_state = None
    action = None
    select_mode = False  # Режим, когда уже задали впорос с выблром игры
    end_session = False

    def __init__(self, action, select_mode, game_name, game_state) -> None:
        self.action = action
        self.select_mode = select_mode
        self.game_name = game_name

        if game_name:
            state_cls = get_game_state_class(game_name)
            self.game_state = state_cls(game_state)
        else:
            self.action = 'select_game'

    def get_action(self):
        """ Вернуть название обработчика, который нужно вызвать в текущей игре """
        return self.action or self.game_state.action

    def serialize(self):
        return dict(
            action=self.action,
            select_mode=self.select_mode,
            game_name=self.game_name,
            game_state=self.game_state.serialize() if self.game_state else None,
        )

