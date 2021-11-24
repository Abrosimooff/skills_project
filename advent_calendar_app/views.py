import datetime
import json

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView

from advent_calendar_app.logic import AdventCalendarTasks
from core.views.mrc import MRCView
from core.wrappers.mrc import MRCMessageWrap
from advent_calendar_app.processor import AdventCalendarProcessor


class MRCSkillAdventCalendarView(MRCView):
    """ Handler Скилла "Advent Calendar" """

    def get(self, request, *args, **kwargs):
        return HttpResponse('OK')

    def post(self, request, *args, **kwargs):
        request_message = json.loads(request.body)
        message = MRCMessageWrap(request_message)
        processor = AdventCalendarProcessor()
        response = processor.process(message, hook_day=self.request.GET.get('hook_day'))
        return JsonResponse(response.serialize())


class CalendarTaskView(TemplateView):
    """ Задание """
    template_name = 'advent_calendar_app/day.jinja'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        from hashids import Hashids
        hashids = Hashids()
        if kwargs.get('slug'):
            age, day = hashids.decode(kwargs.get('slug'))
            # age, day = 8,  4 # todo test
            task = AdventCalendarTasks(age).get_by_day(day)
            ctx.update(
                age=age,
                day=day,
                task=task
            )
        return ctx

