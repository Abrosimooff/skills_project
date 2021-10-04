from __future__ import unicode_literals, absolute_import, division, print_function

import json
from django.http import HttpResponse, JsonResponse

from core.views.mrc import MRCView
from core.wrappers.mrc import MRCMessageWrap, ActionResponse, MRCResponse, MRCResponseDict


class MRCTestView(MRCView):
    """ Простая тестовая вьюха для отладки  """

    def get(self, request, *args, **kwargs):
        return HttpResponse('OK')

    def post(self, request, *args, **kwargs):
        request_message = json.loads(request.body)
        message = MRCMessageWrap(request_message)

        tts = message.request.command
        action_response = ActionResponse(tts=tts)

        response = MRCResponse(
            response=MRCResponseDict(
                text=action_response.text,
                end_session=False,
                tts=action_response.tts
            ),
            session=message.session,
            version=message.version,
            session_state=None
        )
        return JsonResponse(response.serialize())
