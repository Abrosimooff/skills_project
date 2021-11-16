import random
from core.utils.base import audio


class AdventCalendarAudio:
    """ Звуки скилла """
    A1 = '-2000512032_456239036'
    A2 = '-2000512032_456239037'
    A3 = '-2000512032_456239039'
    AUDIO_LIST = [A1, A2, A3]

    @classmethod
    def get_random(cls):
        id = random.choice(cls.AUDIO_LIST)
        return audio(audio_vk_id=id)