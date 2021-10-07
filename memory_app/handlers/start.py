from functools import cached_property

from core.phrases import NEW_GAME_PHRASES
from core.utils.base import clean_text
from core.wrappers.mrc import ActionResponse, Button
from memory_app.const.game import Games, Game
from memory_app.handlers import MemoryAppMRCHandler
from memory_app.states.general import MemoryGameGeneralState


class MemoryAppSelectGame(MemoryAppMRCHandler):
    """ Хэндлер приветствия и выбора игры """
    name = 'select_game'

    def check_game_name(self) -> Game:
        """ Проверить какую игру выбрал юзер """
        user_command = clean_text(self.message.request.command)
        for game in Games.get_game_list():
            for name in game.checked_names:
                if name in user_command:
                    return game

    @property
    def is_repeat(self):
        """ Ответ на вопрос - Сыграем ещё?  """
        user_text = clean_text(self.message.request.command)
        for item in NEW_GAME_PHRASES:
            if item.lower() in user_text:
                return True
        return False

    def check_exit(self):
        user_command = clean_text(self.message.request.command)
        return 'выход' in user_command

    def new_game(self, game: Game) -> ActionResponse:
        """ Новая игра """

        # подмена state на новый
        self.state = MemoryGameGeneralState(
            action=None,
            select_mode=False,
            game_name=game.name,
            game_state={}
        )
        handler = MemoryAppMRCHandler.get_handler(self.state.get_action())
        action_response = handler(message=self.message, state=self.state).action()
        return action_response

    @cached_property
    def buttons(self):
        return [Button('Запоминай слова'), Button('Запоминай рассказ'), Button('Выход')]

    def action(self, **kwargs):
        if not self.state.select_mode:
            self.state.select_mode = True
            return ActionResponse(tts='У меня есть ^две игры^ на тренеровку памяти. '
                                      '«Запоминай слова» и «Запоминай рассказ»! Во что поиграем? ', buttons=self.buttons)
        else:
            game = self.check_game_name()

            # Если есть запущеная игра и select_mode включен. Значит пользователь выбрает играть ли снова?
            if self.state.game_name:
                if self.is_repeat:
                    game = Games.get_game_by_name(self.state.game_name)

            if game:  # Запускаем игру
                return self.new_game(game)
            elif self.check_exit():
                self.state.end_session = True
                return ActionResponse(tts='До сви`дания! Возвращайтесь ещё, потренеровать память.')
            else:
                return ActionResponse('Выберите игру! «Запоминай слова» или «Запоминай рассказ» ? '
                                      'Или скажите: «Выход», чтобы закончить.', buttons=self.buttons)
