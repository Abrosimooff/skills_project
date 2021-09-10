from __future__ import unicode_literals, absolute_import, division, print_function

from memory_app.states.base import MemoryGameStateBase


class ReverseGameState(MemoryGameStateBase):
    """ Игра наоборот - 5 раундов - запоминаем от 3 до 8 слов, нужно назвать строго от последнего к первому
        Состояние
    """
