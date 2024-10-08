from __future__ import unicode_literals, absolute_import, division, print_function

import random
from typing import AnyStr

from colors_app.const import COLOR_MIX
from core.phrases import SIMPLE_REPEAT_PHRASES, NEW_GAME_PHRASES
from core.utils.base import get_score_text, clean_text
from core.utils.const import MRC_EXIT_COMMAND
from core.utils.handlers import MRCHandler
from core.wrappers.mrc import MRCMessageWrap, MRCResponse, MRCResponseDict, ActionResponse, Button


class ColorState:
    questions = None    # Заданные вопросы в этой сессии
    try_count = None    # Номер попытки текущего вопроса
    scores = None       # Баллы в этой сессии
    MAX = 5             # Количество вопрос в 1 игре
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
        score_str = get_score_text(self.scores)
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
        text = question.get_text_question()
        return question, text


class ColorsAppMRCHandler(MRCHandler):
    """ Базовый хэндлер скилла красочки """


class ColorMixHandler(ColorsAppMRCHandler):
    """ Обработчик ответа на вопрос "Играем ещё раз ?" """
    name = 'handle_color_mix'

    @property
    def is_repeat_request(self):
        """ если это запрос на повторение вопроса """
        for phrase in SIMPLE_REPEAT_PHRASES:
            if phrase.lower() in str(self.message.request.command.lower()):
                return True
        return False

    @property
    def is_user_looser(self):
        """ если это сдаюсь """
        return clean_text('сдаюсь') in clean_text(self.message.request.command)

    def finish_game(self, prefix_text):
        """ Завершилась игра """
        if self.state.scores == self.state.MAX:
            result_text = 'Поздравляю! У вас ^отличный^ результат!'
        elif self.state.scores == self.state.MAX - 1:
            result_text = 'Поздравляю! У вас ^хороший^ результат!'
        else:
            result_text = ''

        if self.state.scores == 0:
            finish_text = '{} Игра завершена! К сожалению, вы не угадали ни один цвет!\n' \
                       'Попробуем сыграть ещё раз? Да или нет?'.format(prefix_text)
        else:
            finish_text = '{} Игра завершена! {} ^Вы^ набрали ^{}^. Хотите сыграть ещё раз? Да или нет?'\
                .format(prefix_text,
                        result_text,
                        self.state.scores_verbose
                        )

        self.state.action = RepeatHandler.name
        return ActionResponse(tts=finish_text, buttons=[Button('Ещё раз'), Button('Выход')])

    def action(self, **kwargs):
        """ Должен вернуть, что нужно сказать марусе и как изменить стейт  """
        self.state.action = ColorMixHandler.name
        message = self.message

        #  Если не задали ещё вопросов - задаём
        if not self.state.questions:
            question, text = self.state.next_question()
            if kwargs.get('from_repeat'):
                welcome = 'Начинаем заново! Уд`ачи! '
            else:
                welcome = 'Давай поиграем в ^«Угадай цвет»? '\
                          'Я буду называть цвета. '\
                          'А ваша задача отгадать, какой цвет получится, если их смешать...\n'
            return ActionResponse(tts=welcome + text)

        # Пришёл ответ на вопрос
        if self.state.questions:
            index = self.state.questions[-1]
            current_question = COLOR_MIX[index]
            answer = current_question.answer.ru

            # если просит повторить вопрос или говорит "не знаю"
            if self.is_repeat_request:
                question_text = current_question.get_text_question()
                return ActionResponse(
                    tts='Чтобы перейти к следующему вопросу, скажите: «Сдаюсь»!\n А сейчас повторяю вопрос! {}'
                        .format(question_text),
                    buttons=[Button('Сдаюсь')]
                )

            # Если пользователь сдаётся
            if self.is_user_looser:
                if self.state.can_next:
                    question, text = self.state.next_question()
                    new_text_for_voice = 'Запоминайте правильный ответ! ^{}^! Переходим к следующему вопросу! {}'.format(
                        current_question.get_full_answer().capitalize(),
                        text
                    )
                    return ActionResponse(tts=new_text_for_voice)
                else:
                    answer_text = 'Запоминайте правильный ответ! ^{}^!' \
                        .format(current_question.get_full_answer().capitalize())
                    return self.finish_game(answer_text)

            # если угадали
            if current_question.user_answer_is_valid(str(message.request.command)):
                good_text = 'Верно! <speaker audio=\"marusia-sounds/game-win-1\"> Получится {}. '.format(answer)
                self.state.scores += 1
                if self.state.can_next:
                    question, text = self.state.next_question()
                    text_for_voice = '{} Следующий ^вопрос^ — {}'.format(good_text, text.lower())
                    return ActionResponse(tts=text_for_voice)
                else:
                    return self.finish_game(good_text)
            else:  # не угадали

                # Если попытка 1, 2, 3 - то проверяем
                if self.state.try_count < self.state.MAX_TRY_COUNT:

                    question_text = current_question.get_text_question()
                    text_for_voice = 'Неверно! <speaker audio=\"marusia-sounds/game-loss-2\"> Попр`обуйте ещё раз! {}'.format(question_text)
                    self.state.try_count += 1
                    return ActionResponse(tts=text_for_voice)
                else:
                    # Если попытки кончились
                    if self.state.can_next:
                        question, text = self.state.next_question()
                        new_text_for_voice = '<speaker audio=\"marusia-sounds/game-loss-2\"> Правильный ответ — ^{}^! Переходим к следующему вопросу! {}'.format(
                            current_question.get_full_answer(),
                            text
                        )
                        return ActionResponse(tts=new_text_for_voice)
                    else:
                        answer_text = '<speaker audio=\"marusia-sounds/game-loss-2\">Правильный ответ — ^{}^!'\
                            .format(current_question.get_full_answer())
                        return self.finish_game(answer_text)


class RepeatHandler(ColorsAppMRCHandler):
    """ Обработчик ответа на вопрос "Играем ещё раз ?" """
    name = 'handle_repeat'

    @property
    def is_repeat(self):
        user_text = clean_text(self.message.request.command)

        # Если пользователь говорит не хочу не буду нет - тогда точно нет!
        for item in ['не хоч', 'не буд', 'нет']:
            if clean_text(item) in user_text:
                return False

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
            action_response = handler.action(**kw)  # type: ActionResponse
            return action_response
        else:
            # попрощаться
            self.state.end_session = True
            text = 'До сви`дания! Приходите ^ещё^, помешать кр`асочки.'
            return ActionResponse(tts=text)


class ColorProcessor(object):
    """ Процесс обработки сообщения от Маруси и формирование ответа """

    def do_exit(self):
        return MRCResponseDict(text='До сви`дания! Приходите ещё, помешать кр`асочки.', end_session=True)

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
        handler_class = ColorsAppMRCHandler.get_handler(handler_name=state.action)
        handler = handler_class(message=message, state=state)
        mrc_response = handler.process()
        return mrc_response
