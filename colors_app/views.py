import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from colors_app.processor import ColorProcessor
from colors_app.wrap import MRCMessageWrap, MRCResponse, MRCResponseDict


class LocalhostVew(View):
    http_method_names = ['get', 'post', 'options']

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Length, Content-Type, Date'
        return response


class WebHookColorsView(LocalhostVew):
    """ Handler Скилла "Красочки" """

    def get(self, request, *args, **kwargs):
        return HttpResponse('OK')

    def post(self, request, *args, **kwargs):
        request_message = json.loads(request.body)
        message = MRCMessageWrap(request_message)
        processor = ColorProcessor()
        response = processor.process(message)
        return JsonResponse(response.serialize())
