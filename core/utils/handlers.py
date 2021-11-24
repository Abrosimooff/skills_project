from __future__ import unicode_literals, absolute_import, division, print_function

from typing import AnyStr

from core.wrappers.mrc import MRCMessageWrap, MRCResponse, MRCResponseDict, ActionResponse
from core.wrappers.state import BaseUserState, BaseState


class MRCHandler(object):
    """ Все обработчики должы наследоваться от этого """
    name = None

    def __init__(self, message: MRCMessageWrap, state: BaseState, user_state: BaseUserState = None) -> None:
        self.message = message
        self.state = state
        self.user_state = user_state
        # вероятно в BaseUserState можно повесить флаг (нужно ли обновить стейт через user_state_update),
        # а не передавать в ActionResponse

    @classmethod
    def get_handler(cls, handler_name: AnyStr):
        for handler_class in cls.__subclasses__():
            if handler_class.name == handler_name:
                return handler_class

    def action(self, **kwargs):
        # type: () -> ActionResponse
        raise NotImplementedError

    def process(self, **kwargs):
        action_response = self.action(**kwargs)  # type: ActionResponse

        user_state_update = None
        if self.user_state and self.user_state.need_update:
            user_state_update = self.user_state

        return MRCResponse(
            response=MRCResponseDict(
                text=action_response.text,
                end_session=self.state.end_session,
                tts=action_response.tts,
                buttons=action_response.buttons,
                card=action_response.card,
                push=action_response.push
            ),
            session=self.message.session,
            version=self.message.version,
            session_state=self.state if not self.state.end_session else None,
            user_state_update=user_state_update,
        )
