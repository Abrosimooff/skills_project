

class BaseState:
    """ Базовое состояние объекта """
    end_session = False
    action = None

    def serialize(self):
        return {}


class BaseUserState:
    """ Базовое состояние Пользователя """

    def __init__(self) -> None:
        self._initial_data = self.serialize()

    def serialize(self):
        return {}

    @property
    def need_update(self):
        """ Нужно ли обновить данные? Если даныне изменились с момента инициализации """
        return self._initial_data != self.serialize()