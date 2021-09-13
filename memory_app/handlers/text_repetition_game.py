from __future__ import unicode_literals, absolute_import, division, print_function

import random
from fuzzywuzzy import fuzz

from core.phrases import NEW_GAME_PHRASES
from core.utils.base import clean_punctuation, clean_text, get_score_text
from core.wrappers.mrc import ActionResponse
from memory_app.const.texts import TEXT_LIST
from memory_app.handlers import MemoryAppMRCHandler

# todo 2. Звуки игры
# todo 3. Интонации проверить в текстах особенно
# todo 5. Добавить слов и текстов
from memory_app.states.text_repetition_game import TextRepetitionGameState


class MemoryAppTextRepetitionGameRepeatMRCHandler(MemoryAppMRCHandler):
    """ Выбор категории"""
    name = 'text_repetition_game_repeat'

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
            self.state.game_state = TextRepetitionGameState({})
            self.game_state = self.state.game_state
            handler = MemoryAppTextRepetitionGameMRCHandler(message=self.message, state=self.state)
            kw = {'exclude_text_id': self.game_state.text_id}  #  исклчюаем текущий текст в новой игре
            action_response = handler.action(**kw)  # type: ActionResponse
            return action_response
        else:
            # todo выход в главное меню
            # попрощаться
            self.state.end_session = True
            text = 'До сви`дания! Надеюсь, вам было интересно потренеровать свою память!'
            return ActionResponse(tts=text)


class MemoryAppTextRepetitionGameMRCHandler(MemoryAppMRCHandler):
    """ Выбор категории"""
    name = 'text_repetition_game_process'

    def get_current_text_line(self):
        if self.game_state.text_id is not None and self.game_state.text_line is not None:
            text = TEXT_LIST[self.game_state.text_id][self.game_state.text_line]
            return text

    def get_next_text_line(self, exclude_text_id=None):
        """ Получить следующую строчку для чтения (или первую) """

        def new_text_id():
            """ Рандомно выбрать текст """
            id = None
            while id == exclude_text_id:  # исключить текст = exclude_text_id
                id = random.choice(list(range(len(TEXT_LIST))))
                return id

        if self.game_state.text_id is None:
            text_id = new_text_id()
            self.game_state.text_id = text_id
            self.game_state.text_line = -1

        text = TEXT_LIST[self.game_state.text_id]

        if len(text) > self.game_state.text_line + 1:
            self.game_state.text_line += 1
            text_line = text[self.game_state.text_line]
            return text_line

    def action(self, **kwargs):
        exclude_text_id = kwargs.get('exclude_text_id')
        if self.game_state.text_id is None:  # Если текст не выбран - то начинаем
            text_line = self.get_next_text_line(exclude_text_id)
            if text_line:
                text = 'Сейчас я буду зачитывать небольшой текст! '\
                       'После того как я прочитаю предложение, вы должны будете его повторить! '\
                       'Затем, я прочитаю следующее предложение! Вы повторите! И так далее... Я начинаю! '
                return ActionResponse(text=text, tts=text+text_line)

            else:
                # todo
                return ActionResponse(tts='Ой... проблемка..')

        else:  # Если текст уже читаем
            text = self.get_current_text_line()
            cleaned_text = clean_punctuation(text)
            cleaned_user_command = clean_punctuation(self.message.request.command)
            percent = fuzz.ratio(cleaned_text, cleaned_user_command)
            self.game_state.scores.append(percent)
            text_line = self.get_next_text_line()
            audio = '<speaker audio=marusia-sounds/game-ping-1>'
            if text_line:
                return ActionResponse(text='Запоминайте следующее предложение.', tts=audio+text_line)
            else:
                self.game_state.action = 'text_repetition_game_repeat'
                repeat_text = 'Сыграем ещё раз?'
                avg_score = round(sum(self.game_state.scores) / len(self.game_state.scores))
                score_text = get_score_text(avg_score)

                if avg_score > 90:
                    avg_score = 100
                    score_text = get_score_text(avg_score)
                    return ActionResponse(tts='<speaker audio=marusia-sounds/game-win-2> '
                                              'Игра завершена! Поздравляю! '
                                              'Вы отлично справились с задачей и набрали все {} {}! {}'
                                          .format(avg_score, score_text, repeat_text))
                elif avg_score > 75:
                    return ActionResponse(tts='<speaker audio=marusia-sounds/game-win-2>'
                                              'Игра завершена! Поздравляю! '
                                              'Вы хорошо справились с задачей и набрали {} {}! {}'
                                          .format(avg_score, score_text, repeat_text))
                else:
                    return ActionResponse(tts='<speaker audio=marusia-sounds/game-loss-3> Игра завершена! Вы набрали {} {}! {}'
                                          .format(avg_score, score_text, repeat_text))
