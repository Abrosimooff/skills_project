from __future__ import unicode_literals, absolute_import, division, print_function

from core.utils.handlers import MRCHandler
from core.wrappers.mrc import MRCMessageWrap
from memory_app.states.general import MemoryGameGeneralState


class MemoryAppMRCHandler(MRCHandler):
    """ Базовый хэндлер скилла "Запоминайка" """

    def __init__(self, message: MRCMessageWrap, state: MemoryGameGeneralState) -> None:
        super(MemoryAppMRCHandler, self).__init__(message, state)
        self.message = message
        self.state = state
        self.game_state = self.state.game_state

