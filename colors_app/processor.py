from __future__ import unicode_literals, absolute_import, division, print_function

import random

from colors_app.const import COLOR_MIX, COLOR_RU
from colors_app.wrap import MRCMessageWrap, MRCResponse, MRCResponseDict

MRC_EXIT_COMMAND = "on_interrupt"


class ColorState():
    questions = None    # Заданные вопросы в этой сессии
    try_count = None    # Номер попытки текущего вопроса
    scores = None       # Баллы в этой сессии
    MAX = 5

    def __init__(self, questions, try_count, scores) -> None:
        self.questions = questions
        self.try_count = try_count
        self.scores = scores
        self.end_session = False

    def serialize(self):
        return dict(
            questions=self.questions,
            try_count=self.try_count,
            scores=self.scores,
        )

    @property
    def can_next(self):
        return len(self.questions) < self.MAX

    def process(self, message: MRCMessageWrap):
        """ Должен вернуть, что нужно сказать марусе и как изменить стейт  """

        # todo 1. Учесть несколько вариантов правильных ответов (жолтый, жёлтый и желтый)
        # todo 2. Ударения в цветах и текстах
        # todo 3. Играть ещё раз
        # todo 4. Выходить из игры
        # todo 5. Вынести базу в core

        #  Если не задали ещё вопросов - задаём
        if not self.questions:
            question, text = self.next_question()
            return text

        # Пришёл ответ на вопрос
        if self.questions:
            index = self.questions[-1]
            current_question = COLOR_MIX[index]
            answer = self.get_ru(current_question['answer'])

            # если угадали
            if answer.lower() in str(message.request.command).lower() :
                # угадали
                good_text = 'Верно! <speaker audio=\"marusia-sounds/game-win-1\"> Получится {}. '.format(answer)
                self.scores += 1
                if self.can_next:
                    question, text = self.next_question()
                    new_text = '{} Следующий ^вопрос^ - {}'.format(good_text, text)
                    return new_text
                else:
                    new_text = '{} Игра завершена! ^Вы^ набрали ^{}^ баллов.'.format(good_text, self.scores)
                    self.end_session = True
                    return new_text

            else:  # не угадали

                # Если попытка 1, 2, 3 - то проверяем
                if self.try_count < 3:

                    question_text = self.get_text_question(current_question)
                    text = 'Не верно! <speaker audio=\"marusia-sounds/game-loss-2\"> попр`обуйте ещё раз! {}'.format(question_text)
                    self.try_count += 1
                    return text

                else:
                    # Если попытки кончились
                    if self.can_next:
                        question, text = self.next_question()
                        new_text = '<speaker audio=\"marusia-sounds/game-loss-2\"> Правильный ответ - ^{}^! Переходим к следующему вопросу! {}'.format(
                            self.get_full_answer(current_question, ),
                            text
                        )
                        return new_text
                    else:
                        new_text = 'Игра завершена! ^Вы^ набрали ^{}^ баллов.'.format(self.scores)
                        self.end_session = True
                        return new_text

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

    @staticmethod
    def get_ru(color):
        return COLOR_RU[color]

    def get_full_answer(self, question):
        text = "Если смешать {} и {}, то получится {}".format(
            self.get_ru(question['mix'][0]),
            self.get_ru(question['mix'][1]),
            self.get_ru(question['answer']),
        )
        return text

    def get_text_question(self, question):

        text = "Какой цвет получится - если смешать ^{}^ - и ^{}^?".format(
            self.get_ru(question['mix'][0]),
            self.get_ru(question['mix'][1])
        )
        return text


class ColorProcessor(object):
    """ Процесс обработки сообщения от Маруси и формирование ответа """

    def do_exit(self):
        return MRCResponseDict(text='До сви`дания! Приходите ещё, помешать кр`асочки', end_session=True)

    def process(self, message:MRCMessageWrap) -> MRCResponse:

        print(message.request.command)
        print(message.request.original_utterance)

        # Если сигнал - что пользователь вышел из скилла
        if message.request.command == MRC_EXIT_COMMAND:
            _response_dict = self.do_exit()
            return MRCResponse(
                response=_response_dict,
                session=message.session,
                version=message.version
            )

        #  Если нету стейта сессии
        elif not message.state.session:

            new_state = ColorState(questions=[], try_count=0, scores=0)
            text = new_state.process(message)

            #  Если только начали сессию пох
            # if message.session.new:

            welcome = 'Давай поиграем в ^красочки^? '\
                      'Я буду называть цвета. '\
                      'А ваша задача отгадать, какой цвет получится, если их смешать...'
            new_text = welcome + text
            return MRCResponse(
                response=MRCResponseDict(text=new_text, end_session=new_state.end_session),
                session=message.session,
                version=message.version,
                session_state=new_state
            )

        #  Если есть стейт сессии
        elif message.state.session:
            state = ColorState(
                questions=message.state.session['questions'],
                try_count=message.state.session['try_count'],
                scores=message.state.session['scores'],
            )
            text = state.process(message)

            return MRCResponse(
                response=MRCResponseDict(text=text, end_session=state.end_session),
                session=message.session,
                version=message.version,
                session_state=state if not state.end_session else None
            )