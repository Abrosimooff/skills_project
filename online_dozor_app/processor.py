from __future__ import unicode_literals, absolute_import, division, print_function

import re

from core.utils.base import clean_text
from core.utils.const import MRC_EXIT_COMMAND
from core.utils.handlers import MRCHandler
from core.wrappers.mrc import MRCResponseDict, MRCMessageWrap, MRCResponse, ActionResponse
from memory_app.handlers import MemoryAppMRCHandler
from online_dozor_app.logic import OnlineDozor, DigitDetector


class OnlineDozorState:
    """ Состояние текущего разговора """
    door_number = None
    sms_is_sended = False
    action = None
    end_session = False

    def __init__(self, door_number=None, sms_is_sended=False, action=None) -> None:
        self.door_number = door_number
        self.sms_is_sended = sms_is_sended
        self.action = action or AuthHandler.name

    def serialize(self):
        return dict(
            door_number=self.door_number,
            sms_is_sended=self.sms_is_sended,
            action=self.action,
        )


class OnlineDozorHandler(MRCHandler):
    """ Базовый хэндлер онайлн дозора """
    pass


class AuthHandler(OnlineDozorHandler):
    name = 'auth_handler'

    def good_auth(self):
        """ При успешной авторизации """
        self.state.action = SelectDoorHandler.name
        return ActionResponse(tts='Открыть «Гл`авную^ дверь» или «Дверь во двор»?')

    def get_valid_code(self):
        """ Извлечь из слов пользователя рабочий код из СМС """
        user_text = clean_text(self.message.request.command)

        def f1():
            """ Если в тексте прям цифры """
            digit_list = re.findall('\d+', user_text)
            return digit_list

        def f2():
            """ Если в тексте цифры буквами """
            digit_list = DigitDetector.detect(user_text)
            return [str(x) for x in digit_list]

        digit_string = ''.join(f1())
        if len(digit_string) == 4:
            return digit_string

        digit_string = ''.join(f2())
        if len(digit_string) == 4:
            return digit_string

    def action(self, **kwargs):
        logic = OnlineDozor()

        # Если нет авторизации
        if not logic.auth_info:

            if not self.state.sms_is_sended:  # Если СМС ещё не отпарвили на телефон - отпарвялем

                success = logic.send_code_to_phone_for_auth()
                if success:
                    self.state.sms_is_sended = True
                    return ActionResponse(tts='Нужно быстренько авторизоваться! Я отправила код вам на телефон! '
                                              'Код состоит из четырёх цифр! Продиктуйте мне каждую цифру по-очереди')
                else:
                    self.state.end_session = True
                    return ActionResponse(tts='Извините, я не смогла отправить код для авторизации.')

            else:  # Если СМС уже отправили - распознаём код
                code = self.get_valid_code()
                if code is None:
                    return ActionResponse(tts='Не поняла код! Он должен состоять из четырёх цифр! Продиктуйте ещё раз')
                else:
                    success = logic.send_code_to_site_for_auth(code)
                    if success:
                        return self.good_auth()
                    else:
                        self.state.end_session = True
                        return ActionResponse(tts='Извините, код не подошёл или произвошла другая ошибка.')
        else:
            return self.good_auth()


class SelectDoorHandler(OnlineDozorHandler):
    name = 'select_door_handler'

    def action(self, **kwargs):
        user_text = clean_text(self.message.request.command)
        for item in ['перв', 'глав', 'перед']:
            if clean_text(item) in user_text:
                self.state.door_number = 0  # первая
                break
        if self.state.door_number is None:
            self.state.door_number = 1  # вторая

        logic = OnlineDozor()
        is_opened = logic.process_open_door(self.state.door_number)
        self.state.end_session = True
        door_name = '«Главная дверь»' if self.state.door_number == 0 else '«Дверь во двор»'
        if is_opened:
            return ActionResponse(tts='{} успешно открыта'.format(door_name))
        else:
            return ActionResponse(tts='Не получилось')


class OnlineDozorProcessor(object):

    def do_exit(self):
        return MRCResponseDict(text='Пока', end_session=True)

    def get_state(self, message: MRCMessageWrap) -> OnlineDozorState:
        if message.state.session:
            return OnlineDozorState(
                door_number=message.state.session.get('door_number'),
                sms_is_sended=message.state.session.get('sms_is_sended', False),
                action=message.state.session.get('action'),
            )
        return OnlineDozorState()

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
        handler_class = OnlineDozorHandler.get_handler(handler_name=state.action)
        handler = handler_class(message=message, state=state)
        mrc_response = handler.process()
        return mrc_response
