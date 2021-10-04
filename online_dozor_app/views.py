import json

from django.http import HttpResponse, JsonResponse
from core.views.mrc import MRCView
from core.wrappers.mrc import MRCMessageWrap
from online_dozor_app.processor import OnlineDozorProcessor


class MRCOnlineDozorView(MRCView):
    """ Handler Скилла "Домофон" """

    def get(self, request, *args, **kwargs):
        return HttpResponse('OK')

    def post(self, request, *args, **kwargs):
        request_message = json.loads(request.body)
        message = MRCMessageWrap(request_message)
        processor = OnlineDozorProcessor()
        response = processor.process(message)
        return JsonResponse(response.serialize())
