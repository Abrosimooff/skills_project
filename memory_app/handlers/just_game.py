from __future__ import unicode_literals, absolute_import, division, print_function

import random

from django.utils.functional import cached_property

from core.phrases import NEW_GAME_PHRASES
from core.utils.base import clean_text, get_score_text
from core.wrappers.mrc import ActionResponse
from memory_app.const.categories import CATEGORIES
from memory_app.const.game import WORD_RU, NEXT_ROUND_WORDS
from memory_app.handlers.base import MemoryAppMRCHandler
from memory_app.states.just_game import JustGameState


class MemoryAppJustGameCategorySelectMRCHandler(MemoryAppMRCHandler):
    """ Выбор категории"""
    name = 'just_game_category_select'

    def action(self, **kwargs):
        if not self.game_state.category:  # Если категория не выбрана
            self.game_state.action = 'just_game_category_check'

            category_text = 'У меня есть слова из категорий - "дом", "еда" и "природа"! '\
                            'Выберите одну из этих категорий или скажите "всё", '\
                            'чтобы играть со всеми категориями сразу.'

            next_round_text = NEXT_ROUND_WORDS[2]
            next_round_text2 = NEXT_ROUND_WORDS[3]

            if kwargs.get('from_repeat'):
                tts = 'Выбираем тему для игры и по`ехали! {}'.format(category_text)
            else:
                tts = 'Игра проходит в 5 раундов, в которых вам нужно запоминать мои слова! '\
                      'А затем повторить их! Если не можете закончить раунд - скажите "{}" или "{}"! ' \
                      'Давайте `выбирем тему для игры? {}'.format(next_round_text, next_round_text2, category_text)

            return ActionResponse(tts=tts)


class MemoryAppJustGameCategoryCheckMRCHandler(MemoryAppMRCHandler):
    name = 'just_game_category_check'

    @cached_property
    def selected_category(self):
        """ Проверить какую категорию выбрал пользователь """
        user_category_text = self.message.request.command.lower()
        for category in CATEGORIES:
            for category_name in category.check_names:
                if category_name in user_category_text:
                    index = CATEGORIES.index(category)
                    return index

    def action(self, **kwargs):
        if self.selected_category is not None:
            self.game_state.category = self.selected_category
            handler = MemoryAppJustGameProcessMRCHandler(self.message, self.state)
            action_response = handler.action()
            return action_response
        else:
            return ActionResponse(tts='Я не поняла, какую вы хотите выбрать категорию — '
                                      '"дом", "еда" или "природа" ? '
                                      'Выберите одну из этих категорий или скажите "всё", '
                                      'чтобы играть со всеми категориями сразу.')


class MemoryAppJustGameRepeatMRCHandler(MemoryAppMRCHandler):
    """ Выбор повтор игры """
    name = 'just_game_repeat'

    @property
    def is_repeat(self):
        user_text = clean_text(self.message.request.command)
        for item in NEW_GAME_PHRASES:
            if item.lower() in user_text:
                return True
        return False

    def action(self, **kwargs):
        if self.is_repeat:
            # Сбросит state и вернуть текст новой игры
            self.state.game_state = JustGameState({})
            self.game_state = self.state.game_state
            handler = MemoryAppJustGameCategorySelectMRCHandler(message=self.message, state=self.state)
            kw = {'from_repeat': True}
            action_response = handler.action(**kw)  # type: ActionResponse
            return action_response
        else:
            self.state.end_session = True
            text = 'До сви`дания! Надеюсь, вам было интересно потренеровать свою память!'
            return ActionResponse(tts=text)


class MemoryAppJustGameProcessMRCHandler(MemoryAppMRCHandler):
    name = 'just_game_process'

    @property
    def next_words_count(self):
        """ Сколько слов нужно для следующего раунда """
        START_WORD_COUNT = self.game_state.WORDS_ROUNDS[0]
        words_count = len(self.game_state.words) + 1 if len(self.game_state.words) else START_WORD_COUNT
        return words_count

    @property
    def current_round(self):
        """ Какой сейчас раунд """
        if self.game_state.words:
            MIN = self.game_state.WORDS_ROUNDS[0]
            round_num = len(self.game_state.words) - MIN + 1
            return round_num

    @property
    def can_next_round(self):
        """  Можно ли начинать следующий раунд """
        MAX = len(self.game_state.WORDS_ROUNDS)
        return self.current_round and self.current_round < MAX

    def generate_words(self, category_index, count):
        """ Сгенерить слова для раунда """
        category = CATEGORIES[category_index]
        new_words = random.sample(category.words, count)
        # new_words_ids = map(lambda word: category.words.index(word), new_words)
        return new_words

    @property
    def words_for_check(self):
        """ Слова дял првоерки """
        return set(self.game_state.words) - set(self.game_state.answered_words or [])

    def check_words(self):
        """ Проверить слова от пользователя """
        words_for_check = self.words_for_check
        answered_words = []
        for word in words_for_check:
            cleaned_word = clean_text(word)
            if cleaned_word in clean_text(self.message.request.command):
                answered_words.append(word.lower())

        self.game_state.answered_words.extend(answered_words)
        self.game_state.scores += len(answered_words)
        return answered_words

    @cached_property
    def is_skip_round(self):
        """ Пользователь захотел перейт ик следующему раунду """
        user_command = self.message.request.command.lower()
        for word in NEXT_ROUND_WORDS:
            if word in user_command:
                return True
        return False

    def get_word_ru(self, count):
        """ Получить русское название "5 слов/1 слово" """
        word_ru = WORD_RU.get(count, 'слов')
        return '{} {}'.format(count, word_ru)

    def new_round(self):
        """ Начинаем новый раунд, возвращаю текст новых слов """
        new_words = self.generate_words(self.game_state.category, self.next_words_count)
        self.game_state.words = new_words
        self.game_state.try_count = 0
        self.game_state.answered_words = []

        new_words_prepared = map(lambda word: '^%s^' % word, new_words)
        new_words_text = '! '.join(new_words_prepared)
        return new_words_text

    def game_over(self):
        """ Закончить игру """
        # self.state.end_session = True
        self.game_state.action = 'just_game_repeat'

        repeat_text = 'Сыграем ещё?'
        score_text = get_score_text(self.game_state.scores)
        # max 25 score

        audio = '<speaker audio=marusia-sounds/game-win-2>'
        if self.game_state.scores > 20:
            result_text = 'Это отличный результат!'
        elif self.game_state.scores > 15:
            result_text = 'Это хороший результат!'
        else:
            audio = '<speaker audio=marusia-sounds/game-loss-3>'
            result_text = 'Вам есть к чему стремиться!'

        return ActionResponse(tts='Вот и подошёл к концу последний раунд! Я готова объявить результат игры. '
                                  'Вы набрали {} {}! {} {} Спасибо за игру! {}'
                              .format(self.game_state.scores, score_text, audio, result_text, repeat_text))

    def action(self, **kwargs):
        self.game_state.action = self.name

        if self.is_skip_round:  # Если пользователь хочет пропустить раунд

            if self.can_next_round:  # Если можно начать новый раунд
                answered_words = self.game_state.answered_words
                new_words_text = self.new_round()
                text = 'В этом раунде вы угадали {}! Переходим к следующему! ' \
                       'Раунд номер {}! Запоминайте слова! Поехали!'.format(
                    self.get_word_ru(len(answered_words)),
                    self.current_round
                )
                return ActionResponse(text=text,
                                      tts='В этом раунде вы угадали {}! .'
                                          'Переходим к следующему! Раунд номер {}! '
                                          'Запоминайте слова! Поехали! {}.'.format(
                                          self.get_word_ru(len(answered_words)),
                                          self.current_round,
                                          new_words_text
                                      )
                                      )
            else:
                return self.game_over()

        # Если нету слов - то начинаем
        if not self.game_state.words:
            new_words_text = self.new_round()
            text = 'Начинаем первый раунд! Запоминайте слова, затем повторите мне их! Поехали!'
            return ActionResponse(text=text, tts='Начинаем первый раунд! '
                                                 'Запоминайте слова, затем повторите мне их! Поехали! {}'
                                  .format(new_words_text))
        else:

            # Есть заданные слова - мы проверяем ответ пользователя.
            checked_words = self.check_words()
            words_for_check = self.words_for_check

            if not checked_words:  # Если не угадали ни одного слова

                # Если попытки есть
                if self.game_state.try_count < self.game_state.MAX_TRY_COUNT:
                    self.game_state.try_count += 1
                    return ActionResponse(tts='Не нашла вашего ответа среди правильных! Назовите ещё {} '
                                              'или скажите "сдаюсь", чтобы перейти в следующий раунд.'.format(
                        self.get_word_ru(len(words_for_check))
                    )
                    )
                else:
                    # Если попытки кончились

                    if self.can_next_round:  # Можно начать след раунд
                        answered_words = self.game_state.answered_words
                        new_words_text = self.new_round()
                        text = 'В этом раунде вы угадали {}! Переходим к следующему! ' \
                               'Раунд номер {}! Запоминайте слова! Поехали!'.format(
                            self.get_word_ru(len(answered_words)),
                            self.current_round
                        )
                        return ActionResponse(text=text,
                                              tts='В этом раунде вы угадали {}! Переходим к следующему! '
                                                  'Раунд номер {}! Запоминайте слова! Поехали! {}.'.format(
                            self.get_word_ru(len(answered_words)),
                            self.current_round,
                            new_words_text
                        )
                        )
                    else:   # Игра завершена!
                        return self.game_over()

            if words_for_check:
                checked_words = map(lambda word: '^"{}"^'.format(word), checked_words)
                checked_words_text = ', '.join(checked_words)
                return ActionResponse(tts='Хорошо! Я засчитала {}! Назовите ещё {} '
                                          'или скажите "сдаюсь", чтобы перейти в следующий раунд.'.format(
                    # self.get_word_ru(len(checked_words)),
                    checked_words_text,
                    len(words_for_check)
                )
                )
            else:
                if self.can_next_round: # Можно начать след. раунд
                    new_words_text = self.new_round()
                    text = 'Супер! Все слова этого раунда засчитаны! Переходим к следующему! '\
                           'Раунд номер {}! Запоминайте слова!'.format(self.current_round)
                    return ActionResponse(text=text, tts='<speaker audio=marusia-sounds/game-win-2> '
                                                         'Супер! Все слова этого раунда засчитаны! '
                                                         'Переходим к следующему! '
                                                         'Раунд номер {}! Запоминайте слова! {} '.format(
                        self.current_round, new_words_text)
                   )
                else:  # конец игры
                    return self.game_over()
