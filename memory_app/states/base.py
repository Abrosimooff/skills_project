from __future__ import unicode_literals, absolute_import, division, print_function

from typing import Dict, AnyStr


class MemoryGameStateBase:
    name = None
    action = None

    def serialize(self) -> Dict:
        raise NotImplementedError
