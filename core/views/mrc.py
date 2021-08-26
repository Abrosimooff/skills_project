from __future__ import unicode_literals, absolute_import, division, print_function

from django.views import View


class MRCView(View):
    """ Базовая вьюха маруси """
    http_method_names = ['get', 'post', 'options']

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Length, Content-Type, Date'
        return response