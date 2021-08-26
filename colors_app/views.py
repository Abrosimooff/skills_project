import json

from django.http import HttpResponse, JsonResponse
from core.views.mrc import MRCView
from core.wrappers.mrc import MRCMessageWrap
from colors_app.processor import ColorProcessor


class MRCSkillColorsView(MRCView):
    """ Handler Скилла "Красочки" """

    def get(self, request, *args, **kwargs):
        return HttpResponse('OK')

    def post(self, request, *args, **kwargs):
        request_message = json.loads(request.body)
        message = MRCMessageWrap(request_message)
        processor = ColorProcessor()
        response = processor.process(message)
        return JsonResponse(response.serialize())
