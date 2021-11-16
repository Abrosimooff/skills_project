import datetime
from typing import AnyStr, Dict, Optional

from django.utils.functional import cached_property

from advent_calendar_app.consts import TASKS_KIDS, TASKS_OLDS, Task


class AdventCalendarTasks:
    """ задания календаря """

    def __init__(self, age):
        self.age = age

    @cached_property
    def tasks(self) -> Dict:
        """ Список всех заданий для выбранного возраста """
        if self.age < 14:
            return TASKS_KIDS
        return TASKS_OLDS

    def get(self, current_date: datetime.date) -> Optional[Task]:
        key = (current_date.month, current_date.day)
        task = self.tasks.get(key)
        return task
