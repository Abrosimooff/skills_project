from __future__ import unicode_literals, absolute_import, division, print_function

from core.utils.base import tts_to_text


class MetaWrap(object):

    def __init__(self, meta) -> None:
        self.locale = meta['locale']
        self.timezone = meta['timezone']
        self.interfaces = meta['interfaces']


class SessionWrap(object):

    def __init__(self, session) -> None:
        self.session_id = session['session_id']
        self.user_id = session['user_id']  # Это поле устарело, но оно обязательное
        self.skill_id = session['skill_id']
        self.new = session['new']
        self.message_id = session['message_id']
        self.user = session.get('user')
        self.application = session['application']
        self.auth_token = session['auth_token']

    def serialize(self):
        return dict(
            session_id=self.session_id,
            skill_id=self.skill_id,
            new=self.new,
            message_id=self.message_id,
            user_id=self.user_id,
        )


class RequestWrap(object):

    def __init__(self, request) -> None:
        self.command = request['command']
        self.original_utterance = request['original_utterance']
        self.type = request['type']
        self.payload = request.get('payload')
        self.nlu = request['nlu']


class StateWrap(object):
    session = None  # состояние внутри сессии
    user = None     # состояние внутри пользователя

    def __init__(self, state) -> None:
        """ Оба могут отсутствовать """
        self.session = state.get('session')
        self.user = state.get('user')


class MRCMessageWrap(object):
    """ Сообщение от Маруси """

    def __init__(self, message) -> None:
        self.meta = MetaWrap(message['meta'])
        self.request = RequestWrap(message['request'])
        self.session = SessionWrap(message['session'])
        self.version = message['version']
        self.state = StateWrap(message.get('state', {}))


class MRCResponseDict(object):

    def __init__(self, text, end_session, tts=None, buttons=None, card=None) -> None:
        self.text = text
        self.end_session = end_session
        self.tts = tts

    def serialize(self):
        response = dict(
            text=self.text,
            end_session=self.end_session,
        )
        if self.tts:
            response['tts'] = self.tts

        return response


class MRCResponse(object):
    """ Ответ Марусе"""

    def __init__(self, response: MRCResponseDict, session: SessionWrap, version: int,
                 session_state=None , user_state=None) -> None:
        self.response = response
        self.session = session
        self.version = version
        self.session_state = session_state
        self.user_state = user_state

    def serialize(self):
        data = dict(
            response=self.response.serialize(),
            session=self.session.serialize(),
            version=self.version,
        )
        if self.session_state:
            data['session_state'] = self.session_state.serialize()
        if self.user_state:
            data['user_state_update'] = self.user_state
        return data


class ActionResponse(object):
    """  Ответ MRCHandler в методе action """

    def __init__(self, text=None, tts=None) -> None:
        self.text = text
        self.tts = tts
        if not text and tts:
            self.text = tts_to_text(tts)
