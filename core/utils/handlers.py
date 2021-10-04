from __future__ import unicode_literals, absolute_import, division, print_function

from typing import AnyStr

from core.wrappers.mrc import MRCMessageWrap, MRCResponse, MRCResponseDict, ActionResponse


class MRCHandler(object):
    """ Все обработчики должы наследоваться от этого """
    name = None

    def __init__(self, message: MRCMessageWrap, state) -> None:
        self.message = message
        self.state = state

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
        return MRCResponse(
            response=MRCResponseDict(
                text=action_response.text,
                end_session=self.state.end_session,
                tts=action_response.tts
            ),
            session=self.message.session,
            version=self.message.version,
            session_state=self.state if not self.state.end_session else None
        )
