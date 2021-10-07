from __future__ import unicode_literals, absolute_import, division, print_function

import random
from fuzzywuzzy import fuzz

from core.phrases import NEW_GAME_PHRASES
from core.utils.base import clean_punctuation, clean_text, get_score_text
from core.wrappers.mrc import ActionResponse, Button
from memory_app.const.texts import TEXT_LIST
from memory_app.handlers import MemoryAppMRCHandler


class MemoryAppTextRepetitionGameMRCHandler(MemoryAppMRCHandler):
    """ Выбор категории"""
    name = 'text_repetition_game_process'
    audio_signal = '<speaker audio=marusia-sounds/game-ping-1>'
    
    @property
    def is_skip(self):
        """ Пользователь хочет пропустить текущее предложение ? """
        cleaned_user_command = clean_punctuation(self.message.request.command)
        for item in ['пропусти предложен', 'пропустить предложен']:
            if clean_text(item) in cleaned_user_command:
                return True
        return False

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
        
    def finish(self):
        """ Конец игры """
        self.state.action = 'select_game'
        self.state.select_mode = True
        repeat_text = 'Сыграем ещё раз? Или поиграем в «Запоминай слова»? ' \
                      'Если хотите закончить, скажите: «Выход».'
        buttons = [Button('Ещё раз'), Button('Запоминай слова'), Button('Выход')]

        avg_score = round(sum(self.game_state.scores) / len(self.game_state.scores))
        score_text = get_score_text(avg_score)

        if avg_score > 90:
            avg_score = 100
            score_text = get_score_text(avg_score)
            return ActionResponse(tts='<speaker audio=marusia-sounds/game-win-2> '
                                      'Игра завершена. Поздравляю! '
                                      'Вы отлично справились с задачей и набрали все {} {}! {}'
                                  .format(avg_score, score_text, repeat_text),
                                  buttons=buttons)
        elif avg_score > 75:
            return ActionResponse(tts='<speaker audio=marusia-sounds/game-win-2>'
                                      'Игра завершена. Поздравляю! '
                                      'Вы хорошо справились с задачей и набрали {} {}! {}'
                                  .format(avg_score, score_text, repeat_text),
                                  buttons=buttons)
        else:
            return ActionResponse(tts='<speaker audio=marusia-sounds/game-loss-3> '
                                      'Игра завершена. Вы набрали {} {}. {}'
                                  .format(avg_score, score_text, repeat_text),
                                  buttons=buttons)
        
    def to_next_round(self, percent):
        """ Перейти в следующий раун/предложение """
        
        self.game_state.scores.append(percent)
        text_line = self.get_next_text_line()

        if text_line:
            return ActionResponse(text='Запоминайте следующее предложение.', tts=self.audio_signal + text_line)
        else:
            return self.finish()
        
    def to_repeat_round(self):
        """ Повтоврить раунд """
        current_text_line = self.get_current_text_line()
        text = 'Давайте попробуем ещё разок? Слушайте предложение ещё раз! '
        return ActionResponse(text=text,
                              tts=text + self.audio_signal + current_text_line,
                              buttons=[Button('Пропустить предложение')])
    
    def calc_current_percent(self):
        """ Определить текущий процент совпадения текста """
        current_text_line = self.get_current_text_line()
        cleaned_text = clean_punctuation(current_text_line)
        cleaned_user_command = clean_punctuation(self.message.request.command)
        percent = fuzz.ratio(cleaned_text, cleaned_user_command)
        return percent

    def action(self, **kwargs):
        exclude_text_id = kwargs.get('exclude_text_id')
        if self.game_state.text_id is None:  # Если текст не выбран - то начинаем
            text_line = self.get_next_text_line(exclude_text_id)
            if text_line:
                text = 'Сейчас я буду зачитывать небольшой рассказ по предложениям. ' \
                       'А ваша задача — повторять за мной. ' \
                       'И чем точнее вы повторите, тем больше вы заработаете баллов. ' \
                       'Сможете набрать все 100? Начинаем! '
                return ActionResponse(text=text, tts=text+text_line)

            else:
                return ActionResponse(tts='Ой... проблемка.. Рассказ не найден.')

        else:  # Если текст уже читаем

            if self.is_skip:  # Если пользователь нажал кнопку "Пропустить предложение"
                percent = 0
                return self.to_next_round(percent)
                        
            percent = self.calc_current_percent()  # Определение процента совпадения

            if percent < 30:
                return self.to_repeat_round()
            
            return self.to_next_round(percent)
