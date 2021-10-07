from __future__ import unicode_literals, absolute_import, division, print_function

import random

from django.utils.functional import cached_property

from core.phrases import NEW_GAME_PHRASES
from core.utils.base import clean_text, get_score_text, tts_to_text
from core.wrappers.mrc import ActionResponse, Button
from memory_app.const.categories import CATEGORIES
from memory_app.const.game import WORD_RU, NEXT_ROUND_WORDS, NEXT_ROUND_SUPER_PHRASES, NEXT_ROUND_WORD_COUNT
from memory_app.handlers.base import MemoryAppMRCHandler
from memory_app.states.just_game import JustGameState


class MemoryAppJustGameCategorySelectMRCHandler(MemoryAppMRCHandler):
    """ Выбор категории"""
    name = 'just_game_category_select'

    def action(self, **kwargs):
        if not self.game_state.category:  # Если категория не выбрана
            self.game_state.action = 'just_game_category_check'

            category_text = 'Выберите тему для игры: дом, еда, природа. ' \
                            'Если хотите играть со всеми категориями, скажите: «всё».'
            category_text_tts = 'Выберите тему для игры. Дом. Еда. Природа. ' \
                                'Если хотите играть со всеми категориями, скажите: «всё».'

            next_round_text = NEXT_ROUND_WORDS[2].capitalize()
            next_round_text2 = NEXT_ROUND_WORDS[3].capitalize()

            if kwargs.get('from_repeat'):
                text = category_text
                tts = category_text_tts
            else:
                rules_text = 'В игре 5 раундов. Я называю слова, а вы мне их повторяете! Если не можете ' \
                             'закончить раунд, скажите: «{}» или «{}».'.format(next_round_text, next_round_text2)

                text = '{}\n{}'.format(rules_text, category_text)
                tts = '{}\n{}'.format(rules_text, category_text_tts)
            buttons = [Button('Дом'), Button('Еда'), Button('Природа'), Button('Все темы')]
            return ActionResponse(text=text, tts=tts, buttons=buttons)


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
                                      '«дом», «еда» или «природа» ? '
                                      'Выберите одну из этих категорий или скажите «всё», '
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
            text = 'До сви`дания! Надеюсь, вам было интересно потренеровать свою память.'
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

    def next_round(self) -> ActionResponse:
        """ Ответ - Переход к следующему раунду  """
        answered_words = self.game_state.answered_words

        if not self.words_for_check:
            prefix = random.choice(NEXT_ROUND_SUPER_PHRASES) + '<speaker audio=marusia-sounds/game-win-2>'
        else:
            phrase = random.choice(NEXT_ROUND_WORD_COUNT)
            prefix = '{} {}.'.format(phrase, self.get_word_ru(len(answered_words)))

        new_words_text = self.new_round()  # Вызывать в конце!!! (тут s state записываются уже слова нового раунда)

        text = '{} Переходим к следующему. Раунд номер {}. Запоминайте слова.'.format(prefix, self.current_round)
        audio = '<speaker audio=marusia-sounds/game-ping-1>'
        tts = '{} {} {}'.format(text, audio, new_words_text)
        return ActionResponse(text=text, tts=tts)

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
        return WORD_RU.get(count) or '{} слов'.format(count)

    def new_round(self):
        """ Начинаем новый раунд, возвращаю текст новых слов """
        new_words_list_tts = self.generate_words(self.game_state.category, self.next_words_count)
        new_words_list_cleaned = [tts_to_text(word) for word in new_words_list_tts]
        self.game_state.words = new_words_list_cleaned
        self.game_state.try_count = 0
        self.game_state.answered_words = []

        new_words_prepared = map(lambda word: '%s' % word.capitalize(), new_words_list_tts)
        new_words_text = '! '.join(new_words_prepared)
        return new_words_text

    def game_over(self):
        """ Закончить игру """
        self.state.action = 'select_game'
        self.state.select_mode = True
        repeat_text = 'Сыграем ещё раз? Или поиграем в «Запоминай рассказ»? ' \
                      'Если хотите закончить, скажите: «Выход».'
        buttons = [Button('Ещё раз'), Button('Запоминай рассказ'), Button('Выход')]
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

        return ActionResponse(
            tts='Вот и подошёл к концу последний раунд. Вы набрали {} {}. {} {} Спасибо за игру! {}'
                .format(self.game_state.scores, score_text, audio, result_text, repeat_text),
            buttons=buttons
        )

    def action(self, **kwargs):
        self.game_state.action = self.name

        if self.is_skip_round:  # Если пользователь хочет пропустить раунд

            if self.can_next_round:  # Если можно начать новый раунд
                return self.next_round()
            else:
                return self.game_over()

        # Если нету слов - то начинаем
        if not self.game_state.words:
            new_words_text = self.new_round()
            text = 'Начинаем первый раунд. Запоминайте слова, затем повторите мне их. Поехали!'
            return ActionResponse(text=text, tts='{} {}'.format(text, new_words_text))
        else:

            # Есть заданные слова - мы проверяем ответ пользователя.
            checked_words = self.check_words()
            words_for_check = self.words_for_check

            if not checked_words:  # Если не угадали ни одного слова
                # Если попытки есть
                if self.game_state.try_count < self.game_state.MAX_TRY_COUNT:
                    self.game_state.try_count += 1
                    return ActionResponse(
                        tts='Не нашла вашего ответа среди правильных. Назовите ещё {} или скажите: «Сдаюсь»'
                            .format(self.get_word_ru(len(words_for_check))),
                        buttons=[Button('Сдаюсь')]
                    )
                else:
                    # Если попытки кончились
                    if self.can_next_round:         # Можно начать след раунд
                        return self.next_round()
                    else:                           # Игра завершена!
                        return self.game_over()

            if words_for_check:
                checked_words = map(lambda word: '^{}^'.format(word), checked_words)
                checked_words_text = ', '.join(checked_words)
                return ActionResponse(
                    tts='Хорошо! Я засчитала: {}. Назовите ещё {} или скажите: «Сдаюсь», чтобы перейти в следующий раунд.'
                        .format(checked_words_text, self.get_word_ru(len(words_for_check))),
                    buttons=[Button('Сдаюсь')]
                )
            else:
                if self.can_next_round:  # Можно начать след. раунд
                    return self.next_round()
                else:  # конец игры
                    return self.game_over()
