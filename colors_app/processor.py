from __future__ import unicode_literals, absolute_import, division, print_function

import random
from typing import AnyStr

from colors_app.const import COLOR_MIX, ColorObj, ColorMixObj
from colors_app.phrases import SIMPLE_REPEAT_PHRASES, NEW_GAME_PHRASES
from core.wrappers.mrc import MRCMessageWrap, MRCResponse, MRCResponseDict, ActionResponse

MRC_EXIT_COMMAND = "on_interrupt"


SCORES_STR = {
    0: 'Баллов',
    1: 'Балл',
    2: 'Балла',
    3: 'Балла',
}


class ColorState:
    questions = None    # Заданные вопросы в этой сессии
    try_count = None    # Номер попытки текущего вопроса
    scores = None       # Баллы в этой сессии
    MAX = 3             # Количество вопрос в 1 игре
    MAX_TRY_COUNT = 2   # Количество попыток на 1 вопрос

    def __init__(self, questions, try_count, scores, action) -> None:
        self.questions = questions
        self.try_count = try_count
        self.scores = scores
        self.end_session = False
        self.action = action

    def serialize(self):
        return dict(
            questions=self.questions,
            try_count=self.try_count,
            scores=self.scores,
            action=self.action
        )

    @property
    def can_next(self):
        """ Можно ли задать след. вопрос ?"""
        return len(self.questions) < self.MAX

    @property
    def scores_verbose(self):
        """ Вернопроизвосимое количество баллов "3 балла/ 0 баллов " """
        score_str = SCORES_STR.get(self.scores, 'Баллов')
        return '{} {}'.format(self.scores, score_str)

    def next_question(self):
        """ Ищем вопрос, который ещё не был задан в self.questions  """
        index = None
        question = None
        while question is None:
            _question = random.sample(COLOR_MIX, 1)[0]
            index = COLOR_MIX.index(_question)
            if not index in self.questions:
                question = _question

        self.questions.append(index)
        self.try_count = 1
        text = self.get_text_question(question)
        return question, text

    def get_full_answer(self, question: ColorMixObj) -> AnyStr:
        """ Полный ответ на вопрос """
        text = "Если смешать {} и {}, то получится {}".format(
            question.mix[0].ru,
            question.mix[1].ru,
            question.answer.ru
        )
        return text

    def get_text_question(self, question: ColorMixObj) -> AnyStr:
        """ Текст вопроса """
        index = random.choice((0, 1))
        index2 = 1 if index == 0 else 0
        text = "Какой цвет получится - если смешать ^{}^ - и ^{}^?".format(
            question.mix[index].ru,
            question.mix[index2].ru
        )
        return text


class MRCHandler(object):
    """ Все обработчики должыы наследоваться от этого """
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


class ColorMixHandler(MRCHandler):
    """ Обработчик ответа на вопрос "Играем ещё раз ?" """
    name = 'handle_color_mix'

    @property
    def is_repeat_request(self):
        """ если это запрос на повторение вопроса """
        for phrase in SIMPLE_REPEAT_PHRASES:
            if phrase.lower() in str(self.message.request.command.lower()):
                return True
        return False

    def action(self, **kwargs):
        """ Должен вернуть, что нужно сказать марусе и как изменить стейт  """
        self.state.action = ColorMixHandler.name
        # todo 2. Ударения в цветах и текстах
        # todo 6. аудио не выводить в текст
        message = self.message

        #  Если не задали ещё вопросов - задаём
        if not self.state.questions:
            question, text = self.state.next_question()
            if kwargs.get('from_repeat'):
                welcome = 'Начинаем заново! Уд`ачи! '
            else:
                welcome = 'Давай поиграем в ^красочки^? '\
                          'Я буду называть цвета. '\
                          'А ваша задача отгадать, какой цвет получится, если их смешать...'
            return ActionResponse(welcome + text)

        # Пришёл ответ на вопрос
        if self.state.questions:
            index = self.state.questions[-1]
            current_question = COLOR_MIX[index]
            answer = current_question.answer.ru

            # если просит повторить вопрос
            if self.is_repeat_request:
                question_text = self.state.get_text_question(current_question)
                return ActionResponse('Повторяю вопрос! {}'.format(question_text))

            # если угадали
            if current_question.user_answer_is_valid(str(message.request.command)):
                good_text_for_display = 'Верно! Получится {}. '.format(answer)
                good_text = 'Верно! <speaker audio=\"marusia-sounds/game-win-1\"> Получится {}. '.format(answer)
                self.state.scores += 1
                if self.state.can_next:
                    question, text = self.state.next_question()
                    text_for_display = '{} Следующий ^вопрос^ - {}'.format(good_text_for_display, text)
                    text_for_voice = '{} Следующий ^вопрос^ - {}'.format(good_text, text)
                    return ActionResponse(text_for_display, tts=text_for_voice)
                else:
                    if self.state.scores == self.state.MAX:
                        result_text = 'Поздравляю! У вас ^отличный^ результат!'
                    elif self.state.scores == self.state.MAX - 1:
                        result_text = 'Поздравляю! У вас ^хороший^ результат!'
                    else:
                        result_text = ''
                    new_text = '{} Игра завершена! {} ^Вы^ набрали ^{}^. Хотите сыграть ещё раз? Да или нет?'.format(good_text, result_text, self.state.scores_verbose)
                    self.state.action = RepeatHandler.name
                    return ActionResponse(new_text)

            else:  # не угадали

                # Если попытка 1, 2, 3 - то проверяем
                if self.state.try_count < self.state.MAX_TRY_COUNT:

                    question_text = self.state.get_text_question(current_question)
                    text_for_display = 'Не верно! Попробуйте ещё раз! {}'.format(question_text)
                    text_for_voice = 'Не верно! <speaker audio=\"marusia-sounds/game-loss-2\"> попр`обуйте ещё раз! {}'.format(question_text)
                    self.state.try_count += 1
                    return ActionResponse(text_for_display, tts=text_for_voice)
                else:
                    # Если попытки кончились
                    if self.state.can_next:
                        question, text = self.state.next_question()
                        new_text_for_display = 'Правильный ответ - {}! Переходим к следующему вопросу! {}'.format(
                            self.state.get_full_answer(current_question),
                            text
                        )
                        new_text_for_voice = '<speaker audio=\"marusia-sounds/game-loss-2\"> Правильный ответ - ^{}^! Переходим к следующему вопросу! {}'.format(
                            self.state.get_full_answer(current_question),
                            text
                        )
                        return ActionResponse(new_text_for_display, tts=new_text_for_voice)
                    else:
                        answer_text_for_display = 'Правильный ответ - {}!'\
                            .format(self.state.get_full_answer(current_question))
                        answer_text = '<speaker audio=\"marusia-sounds/game-loss-2\">Правильный ответ - ^{}^!'\
                            .format(self.state.get_full_answer(current_question))

                        if self.state.scores == self.state.MAX:
                            result_text = 'Поздравляю! У вас ^отличный^ результат!'
                        elif self.state.scores == self.state.MAX - 1:
                            result_text = 'Поздравляю! У вас ^хороший^ результат!'
                        else:
                            result_text = ''

                        new_text_for_display = '{} Игра завершена! {} Вы набрали {}. Хотите сыграть ещё раз? Да или нет?' \
                            .format(answer_text_for_display, result_text, self.state.scores_verbose)
                        new_text_for_voice = '{} Игра завершена! {} ^Вы^ набрали ^{}^. Хотите сыграть ещё раз? Да или нет?'\
                            .format(answer_text, result_text, self.state.scores_verbose)
                        self.state.action = RepeatHandler.name
                        return ActionResponse(new_text_for_display, tts=new_text_for_voice)


class RepeatHandler(MRCHandler):
    """ Обработчик ответа на вопрос "Играем ещё раз ?" """
    name = 'handle_repeat'

    @property
    def is_repeat(self):
        user_text = str(self.message.request.command).lower()
        for item in NEW_GAME_PHRASES:
            if item.lower() in user_text:
                return True
        return False

    def action(self, **kwargs):
        if self.is_repeat:
            # Сбросит state и вернуть текст новой игры
            self.state = ColorState([], 0, 0, ColorMixHandler.name)
            handler = ColorMixHandler(message=self.message, state=self.state)
            kw = {'from_repeat': True}
            text = handler.action(**kw)
            return ActionResponse(text)
        else:
            # попрощаться
            self.state.end_session = True
            text = 'До сви`дания! Приходите ^ещё^, помешать кр`асочки'
            return ActionResponse(text)


class ColorProcessor(object):
    """ Процесс обработки сообщения от Маруси и формирование ответа """

    def do_exit(self):
        return MRCResponseDict(text='До сви`дания! Приходите ещё, помешать кр`асочки', end_session=True)

    def get_state(self, message: MRCMessageWrap):
        if message.state.session:
            state = ColorState(
                questions=message.state.session['questions'],
                try_count=message.state.session['try_count'],
                scores=message.state.session['scores'],
                action=message.state.session.get('action'),
            )
        else:
            state = ColorState(questions=[], try_count=0, scores=0, action='handle_color_mix')

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
        handler_class = MRCHandler.get_handler(handler_name=state.action)
        handler = handler_class(message=message, state=state)
        mrc_response = handler.process()
        return mrc_response
