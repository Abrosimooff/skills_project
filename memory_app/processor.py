from __future__ import unicode_literals, absolute_import, division, print_function

from typing import Dict, AnyStr

from core.utils.const import MRC_EXIT_COMMAND
from core.wrappers.mrc import MRCResponseDict, MRCMessageWrap, MRCResponse


# 1. Простая игра - 5 раундов - запоминаем от 3 до 8 слов
# 2. Игра наоборот - 5 раундов - запоминаем от 3 до 8 слов, нужно назвать строго от последнего к первому
# 2. Игра изложение - Пишем несложный текст, предложение за предложением, проверяем точность ответа от пользователя
from memory_app.handlers.base import MemoryAppMRCHandler
from memory_app.states.general import MemoryGameGeneralState


class MemoryProcessor(object):
    """ Процесс обработки сообщения от Маруси и формирование ответа """

    def do_exit(self):
        return MRCResponseDict(text='До сви`дания! Возвращайтесь ещё, потренеровать память.', end_session=True)

    def get_state(self, message: MRCMessageWrap) -> MemoryGameGeneralState:
        session_state = message.state.session or {}

        state = MemoryGameGeneralState(
            action=session_state.get('action'),
            select_mode=session_state.get('select_mode', False),
            game_name=session_state.get('game_name'),
            game_state=session_state.get('game_state'),
        )
        # if message.state.session and message.state.session.get('game_name'):
        #     state = MemoryGameGeneralState.create_game_state(
        #         game_name=message.state.session['game_name'],
        #         game_state=message.state.session['game_state']
        #     )
        # else:
        #     # с чего начинаем!
        #     state = MemoryGameGeneralState.create_init_state()

        return state

    def process(self, message: MRCMessageWrap) -> MRCResponse:

        # Если сигнал - что пользователь вышел из скилла
        if message.request.command == MRC_EXIT_COMMAND:
            _response_dict = self.do_exit()
            return MRCResponse(
                response=_response_dict,
                session=message.session,
                version=message.version
            )

        state = self.get_state(message)
        action = state.get_action()
        handler_class = MemoryAppMRCHandler.get_handler(handler_name=action)
        handler = handler_class(message=message, state=state)
        mrc_response = handler.process()
        return mrc_response
