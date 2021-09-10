from core.utils.base import clean_text
from core.wrappers.mrc import ActionResponse
from memory_app.const.game import Games, Game
from memory_app.handlers import MemoryAppMRCHandler
from memory_app.states.general import get_game_state_class, MemoryGameGeneralState


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

    def action(self, **kwargs):
        if not self.state.select_mode:
            self.state.select_mode = True
            return ActionResponse(tts='У меня есть ^две игры^ на тренеровку памяти! '
                                      '"Запоминай слова" и "Запоминай рассказ"! Какую игру запускаем? ')
        else:
            game = self.check_game_name()
            if game:  # Запускаем игру
                self.state.game_name = game.name
                state = MemoryGameGeneralState(
                    action=None,
                    select_mode=False,
                    game_name=game.name,
                    game_state={}
                )

                self.state = state  # подмена state на новый
                handler = MemoryAppMRCHandler.get_handler(state.get_action())
                action_response = handler(message=self.message, state=state).action()
                return action_response
            else:
                return ActionResponse('Выберите игру! "Запоминай слова" или "Запоминай рассказ" ?')
