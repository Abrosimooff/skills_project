from __future__ import unicode_literals, absolute_import, division, print_function

from typing import AnyStr, List, Dict

from core.utils.base import tts_to_text
from core.wrappers.state import BaseUserState


class Button(object):
    title: AnyStr
    payload: Dict
    url: AnyStr

    def __init__(self, title, payload=None, url=None) -> None:
        self.title = title
        self.payload = payload
        self.url = url

    def serialize(self):
        serialized = dict(
            title=self.title,
        )
        if self.payload:
            serialized['payload'] = self.payload
        if self.url:
            serialized['url'] = self.url
        return serialized


class Card:
    type: AnyStr

    def serialize(self):
        raise NotImplementedError


class CardLink(Card):
    """ Карточка - сылка """
    type = 'Link'
    url: AnyStr
    title: AnyStr
    text: AnyStr
    image_id: int

    def __init__(self, url: AnyStr, title: AnyStr, text: AnyStr, image_id: int) -> None:
        self.url = url
        self.title = title
        self.text = text
        self.image_id = image_id

    def serialize(self):
        return dict(
            type=self.type,
            url=self.url,
            title=self.title,
            text=self.text,
            image_id=self.image_id,
        )


class MetaWrap(object):

    def __init__(self, meta) -> None:
        self.locale = meta['locale']
        self.timezone = meta['timezone']
        self.interfaces = meta['interfaces']
        self._city_ru = meta.get('_city_ru')


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
        self.nlu = request.get('nlu', [])


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

    def __init__(self, text, end_session, tts=None, buttons: List[Button] = None, card: Card = None) -> None:
        self.text = text
        self.end_session = end_session
        self.tts = tts
        self.buttons = buttons or []
        self.card = card

    def serialize(self):
        response = dict(
            text=self.text,
            end_session=self.end_session,
        )
        if self.tts:
            response['tts'] = self.tts
        if self.buttons:
            response['buttons'] = [b.serialize() for b in self.buttons]
        if self.card:
            response['card'] = self.card.serialize()

        return response


class MRCResponse(object):
    """ Ответ Марусе"""

    def __init__(self, response: MRCResponseDict, session: SessionWrap, version: int,
                 session_state=None, user_state_update: BaseUserState = None) -> None:
        self.response = response
        self.session = session
        self.version = version
        self.session_state = session_state
        self.user_state_update = user_state_update

    def serialize(self):
        data = dict(
            response=self.response.serialize(),
            session=self.session.serialize(),
            version=self.version,
        )
        if self.session_state:
            data['session_state'] = self.session_state.serialize()
        if self.user_state_update:
            data['user_state_update'] = self.user_state_update.serialize()
        return data


class ActionResponse(object):
    """  Ответ MRCHandler в методе action """
    text: AnyStr
    tts: AnyStr
    buttons: List
    card: Card

    def __init__(self, text: AnyStr = None, tts: AnyStr = None, buttons: List[Button] = None, card: Card = None) -> None:
        self.text = tts_to_text(text or tts)
        self.tts = tts
        self.buttons = buttons or []
        self.card = card