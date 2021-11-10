import datetime

import pytz
from django.utils.functional import cached_property

from advent_calendar_app.logic import AdventCalendarTasks
from core.utils.base import clean_text
from core.utils.const import MRC_EXIT_COMMAND
from core.utils.handlers import MRCHandler
from core.wrappers.mrc import MRCResponseDict, MRCMessageWrap, MRCResponse, ActionResponse
from core.wrappers.state import BaseUserState, BaseState


class ACState(BaseState):

    def __init__(self, action) -> None:
        self.action = action or 'start'

    def serialize(self):
        return dict(
            action=self.action
        )


class ACUserState(BaseUserState):
    """ постоянно хранимые данные пользовтеля """

    def __init__(self, age: int = None, first_date=None, last_date=None) -> None:
        self.age = age
        self.first_date = first_date
        self.last_date = last_date
        super(ACUserState, self).__init__()

    def serialize(self):
        return dict(
            age=self.age,
            first_date=self.first_date,
            last_date=self.last_date
        )


class AdventCalendarMRCHandler(MRCHandler):
    """ Базовый хэндлер скилла красочки """

    @cached_property
    def today(self) -> datetime.date:
        """ Сегодняшняя дата ПОЛЬЗОВАТЕЛЯ """
        return datetime.date(2021, 12, 1)  # todo test

        user_timezone = pytz.timezone(self.message.meta.timezone)
        user_now = datetime.datetime.now(user_timezone)                          # Текущее Время пользователя
        # user_now_utc = datetime.datetime.utcnow().replace(tzinfo=user_timezone)  # Текущее Время пользователя UTC
        user_date = datetime.date(user_now.year, user_now.month, user_now.day)   # Текущая дата пользователя
        return user_date

    @cached_property
    def tomorrow(self):
        """ Завтрашняя дата ПОЛЬЗОВАТЕЛЯ """
        return self.today + datetime.timedelta(days=1)

    @cached_property
    def new_year_date(self):
        return datetime.date(self.today.year, 12, 31)

    @cached_property
    def days_before_new_year(self) -> int:
        """ Сколько дней до нового года ? """
        return (self.new_year_date - self.today).days

    @cached_property
    def is_active(self):
        """ Активен ли сейчас календарь ? работает с 1 декабря до 31 декабря """
        return self.days_before_new_year <= 31

    def not_active_response(self):
        """ Когда сегодня не декабрь """

        if self.days_before_new_year <= 60:
            text = 'Мы напишем письмо деду морозу, ' \
                   'посмотрим новогодние фильмы и мультфильмы, ' \
                   'сделаем что-то красивое своими руками и выполним ещё много интересных заданий. ' \
                   'Приходите 1 декабря, я буду Вас ждать.'
            tts = 'Мы напишем письмо деду ^морозу^! ' \
                   'Посмотрим новогодние фильмы и мультфильмы! ' \
                   'Сделаем что-то красивое своими руками и выполним ещё много интересных заданий! ' \
                   'Приходите первого декабря, я буду Вас ждать.'
        elif self.days_before_new_year > 350:
            text = 'Поздравляю вас с наступившим новым годом! ' \
                   'Надеюсь, вам понравились мои задания. ' \
                   'Приходите на следующий год.'
            tts = text
        else:
            text = 'До нового года ещё далеко, я буду вас ждать 1 декабря.'
            tts = 'До нового года ещё далеко, я буду вас ждать первого декабря.'

        self.state.end_session = True
        start_text = 'Здравствуйте! Адвент календарь - это список ежедневных заданий в ожидании Нового года. ' \
                     'И начинается он 1 декабря! {}'.format(text)
        start_tts = 'Здравствуйте! Адвент календарь - это список ежедневных заданий в ожидании Нового года. ' \
                    'И начинается он первого декабря! {}'.format(tts)
        return ActionResponse(text=start_text, tts=start_tts)

    def today_response(self, welcome=False):
        if self.is_active:
            calendar = AdventCalendarTasks(self.user_state.age)
            task = calendar.get(self.today)
            task_tomorrow = calendar.get(self.tomorrow)

            if task:
                tts = 'Вот ваше задание на сегодня. {}. '.format(task.text)
                if welcome:
                    tts = 'Желаю Вам приятного ожидания Нового года! ' + tts

                if task_tomorrow and task_tomorrow.text_yesterday:
                    tomorrow_question = '\nНамекнуть какое задание будет завтра?'
                    tts += tomorrow_question
                    self.state.action = 'tomorrow'
                return ActionResponse(tts=tts)
            else:
                return ActionResponse('Задание на сегодня не найдено')  # Такого не должно быть, т.к првоерка is_active
        else:
            return self.not_active_response()


class AdventCalendarStartMRCHandler(AdventCalendarMRCHandler):
    name = 'start'

    def action(self, **kwargs):
        if self.is_active:
            age_question = 'Чтобы я подобрала для вас по настоящему интересные задания, скажите сколько вам лет?'
            self.state.action = 'age'
            return ActionResponse(tts='Здравствуйте! До Нового года осталось совсем немного, '
                                      'я хочу украсить ваше ожидание ^этого^ чудесного праздника! '
                                      'Адвент календарь - это список ежедневных заданий в ожидании Нового года. '
                                      'Я помогу вам готовиться к праздникам, давая приятное и интересное задание! '
                                      'Каждый день — ^новое^!\n' + age_question)
        else:
            return self.not_active_response()
            # if self.days_before_new_year < 60:
            #     text = 'Мы напишем письмо деду морозу, ' \
            #            'посмотрим новогодние фильмы и мульфильмы, ' \
            #            'сделаем что-то красивое своими руками и выполним ещё много интересных заданий. ' \
            #            'Приходите 1 декабря, я буду Вас ждать.'
            # elif self.days_before_new_year > 350:
            #     text = 'Поздравляю вас с наступившим новым годом! ' \
            #            'Надеюсь, вам понравились мои задания. ' \
            #            'Приходите на следующий год.'
            # else:
            #     text = 'До нового года ещё далеко, я буду вас ждать 1 декабря.'
            #
            # self.state.end_session = True
            # return ActionResponse(tts='Здравствуйте! '
            #                           'Адвент календарь - это список ежедневных заданий в ожидании Нового года. '
            #                           'И начинается он 1 декабря! {}'.format(text))


class AdventCalendarAgeMRCHandler(AdventCalendarMRCHandler):
    name = 'age'

    def detect_age(self):
        """ Определить возвраст """
        age = 9
        self.user_state.age = age
        return age

    def action(self, **kwargs):
        age = self.detect_age()
        if age:
            return self.today_response(welcome=True)
        else:
            ActionResponse('Я не расслышала. повторите ещё раз. Сколько вам лет?')


class AdventCalendarTomorrowMRCHandler(AdventCalendarMRCHandler):
    name = 'tomorrow'

    @property
    def is_good(self):
        """ Пользователь хочет, чтобы ему намекнули что будет завтра? """
        user_text = clean_text(self.message.request.command)
        if clean_text('не') in user_text:
            return False

        for item in ['да', 'намекн', 'расска']:
            if clean_text(item) in user_text:
                return True
        return False

    def action(self, **kwargs):
        self.state.action = 'today'
        self.state.end_session = True

        if self.is_good:
            calendar = AdventCalendarTasks(self.user_state.age)
            task_tomorrow = calendar.get(self.tomorrow)
            if task_tomorrow and task_tomorrow.text_yesterday:
                return ActionResponse(tts=task_tomorrow.text_yesterday)
        else:
            return ActionResponse(tts='Поняла. Выполняйте текущее задание. '
                                      'Не буду забивать вам голову заданиями из будущего.')


class AdventCalendarTodayMRCHandler(AdventCalendarMRCHandler):
    name = 'today'

    def action(self, **kwargs):
        return self.today_response(welcome=True)


class AdventCalendarProcessor(object):
    """ Процесс обработки сообщения от Маруси и формирование ответа """

    def do_exit(self):
        return MRCResponseDict(text='До сви`дания! Приходите ещё, помешать кр`асочки.', end_session=True)

    def get_state(self, message: MRCMessageWrap):
        if message.state.session:
            state = ACState(
                action=message.state.session.get('action'),
            )
        else:
            state = ACState(action='start')

        return state

    def get_user_state(self, message: MRCMessageWrap):
        print('message.state.user', message.state.user)
        if message.state.user:
            return ACUserState(
                age=message.state.user.get('age'),
                first_date=message.state.user.get('first_date'),
                last_date=message.state.user.get('last_date'),
            )
        else:
            return ACUserState()

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
        user_state = self.get_user_state(message)
        print('user_state', user_state.serialize())
        handler_class = AdventCalendarMRCHandler.get_handler(handler_name=state.action)
        handler = handler_class(message=message, state=state, user_state=user_state)
        mrc_response = handler.process()
        return mrc_response
