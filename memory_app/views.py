import json

from django.http import HttpResponse, JsonResponse
from core.views.mrc import MRCView
from core.wrappers.mrc import MRCMessageWrap
from memory_app.processor import MemoryProcessor


class MRCMemoryGameView(MRCView):
    """ Handler Скилла "Запоминйка" """

    def get(self, request, *args, **kwargs):
        return HttpResponse('OK')

    def post(self, request, *args, **kwargs):
        request_message = json.loads(request.body)
        message = MRCMessageWrap(request_message)
        processor = MemoryProcessor()
        response = processor.process(message)
        return JsonResponse(response.serialize())
