import json

from django.http import HttpResponse, JsonResponse
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
        response = processor.process(message)
        return JsonResponse(response.serialize())
