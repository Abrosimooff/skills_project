from __future__ import unicode_literals, absolute_import, division, print_function

import pickle
import re
from typing import AnyStr, Dict, NoReturn, Optional, List

import requests

from core.utils.misc import SafeContext
from skills.settings import PHONE_NUMBER


class DigitDetector:
    """ Определятель цифр (от 0 до 9) в строке """
    D0 = 'нол'
    D1 = 'один'
    D2 = 'два'
    D3 = 'три'
    D4 = 'четыр'
    D5 = 'пят'
    D6 = 'шест'
    D7 = 'сем'
    D8 = 'восем'
    D9 = 'девят'

    MAP = {
        D0: 0,
        D1: 1,
        D2: 2,
        D3: 3,
        D4: 4,
        D5: 5,
        D6: 6,
        D7: 7,
        D8: 8,
        D9: 9,
    }

    @classmethod
    def detect(cls, text):
        # type: (AnyStr) -> List[int]
        digits = []
        for key, value in cls.MAP.items():  # Ходим по каждой цифре от 0 до 9
            matches = [SafeContext(value=value, index=item.start()) for item in re.finditer(key, text)]

            if key == cls.D7:  # Если нашли 7, то проверяем чтобы это было не 8
                matches = list(filter(lambda x: x.index < 2 or text[x.index - 2 : x.index] != 'во', matches))

            digits.extend(matches)

        sorted_items = sorted(digits, key=lambda x: x.index)
        return [x.value for x in sorted_items]


class AuthInfo:
    """ Информация после авторизации
         LOGIN, CLIENT_NAME, IS_ADMIN, REGISTER_DT, TOKEN, IS_BUGSHAKER_ENABLED, IS_WIDGET_ENABLED, IS_PAYED, ADDRESS
    """
    login: AnyStr
    token: AnyStr
    client_name: AnyStr

    def __init__(self, data) -> None:
        self.login = data.get('LOGIN')
        self.token = data.get('TOKEN')
        self.client_name = data.get('CLIENT_NAME')


class DoorInfo:
    """ Загруженная информация о дверях (key меняется возможно каждый день) """
    key: AnyStr
    app_id: AnyStr
    type: Dict
    longitude: float
    latitude: float
    description: AnyStr
    overview_camera: Dict
    address: Dict
    open_url: AnyStr

    def __init__(self, data) -> None:
        self.key = data.get('key')
        self.app_id = data.get('app_id')
        self.type = data.get('type')
        self.longitude = data.get('longitude')
        self.latitude = data.get('latitude')
        self.description = data.get('description')
        self.overview_camera = data.get('overview_camera')
        self.address = data.get('address')
        self.open_url = 'https://prx-dev.goodline.info/{}/openDoor'.format(self.app_id)

    def open(self, session):
        """ Работает с пустой сессией  """
        headers = {'x-key': self.key}
        response = session.get(self.open_url, headers=headers)
        # print('response', response)
        # print('content', response.content)
        return response.status_code == 200


class OnlineDozor:
    """ Класс для работы с сайтом онлайн-дозор """
    phone_url = 'https://api-video.goodline.info/ords/mobile/vc2/auth/phone'
    sms_url = 'https://api-video.goodline.info/ords/mobile/vc2/auth/token/sms'
    load_doors_url = 'https://api-video.goodline.info/ords/mobile/dozor/gates'

    auth_info_filename = 'online_dozor_auth_info'
    auth_info = None
    door_list = []

    def __init__(self) -> None:
        self.session = requests.Session()
        self.auth_info = self.load_auth_info()

    def process_auth(self, sms_code=None):
        if not self.auth_info:
            if not sms_code:
                success = self.send_code_to_phone_for_auth()
                print('Отправка кода на телефон -  {}'.format('Успешно' if success else 'Нудачно'))
            else:
                success = self.send_code_to_site_for_auth(str(sms_code))
                print('Авторизация по коду -  {}'.format('Успешно' if success else 'Нудачно'))

    def process_open_door(self, door_index, ):
        """ Весь процесс открытия двери """

        # Если авторизация есть
        if self.auth_info:
            success = self.load_doors()  # todo сохранять
            print('Загрузка списка деверей -  {}'.format('Успешно' if success else 'Нудачно'))

            if success:
                is_opened = self.door_list[door_index].open(self.session)
                print('Дверь открыта -  {}'.format('Успешно' if is_opened else 'Нудачно'))
                return is_opened

    def load_doors(self):
        """ Загрузить двери """
        headers = {'token': self.auth_info.token}
        response = self.session.get(self.load_doors_url, headers=headers)
        if response.status_code == 200:
            self.door_list = [DoorInfo(door_data) for door_data in response.json()]
            return True
        return False

    def save_auth_info(self, auth_info):
        # type: (AuthInfo) -> NoReturn
        """ Сохранить авторизацию в файл """
        with open(self.auth_info_filename, 'wb') as f:
            pickle.dump(auth_info, f)
            print('Данные авторизации сохранены - Успешно')

    def load_auth_info(self):
        # type: () -> Optional[AuthInfo]
        """ Загрузить авторизацию из файла """
        try:
            with open(self.auth_info_filename, 'rb') as f:
                auth_info = pickle.load(f)
                print('Данные авторизации загружены - Успешно')
                return auth_info
        except:
            print('Данные авторизации - Отсутствуют')
            return None

    def send_code_to_phone_for_auth(self):
        # 1. Отправка смс с кодом на телефон

        phone_data = dict(
            phone=PHONE_NUMBER,
            id_device="51eba6dcec0a4",
            id_platform=3
        )
        response = self.session.post(self.phone_url, data=phone_data)
        response_data = response.json()
        sms_lifetime_seconds = response_data['lifetime']  # todo сохранять, чтобы высылать новый
        return response.status_code == 200

    def send_code_to_site_for_auth(self, code_string):
        # 2. Отправка кода из смс на сайт для подтверждения авторизации
        sms_data = dict(
            phone=PHONE_NUMBER,
            code=code_string,
        )
        response = self.session.post(self.sms_url, data=sms_data)
        if response.status_code == 200:
            response_data = response.json()
            self.auth_info = AuthInfo(response_data)
            self.save_auth_info(self.auth_info)
            return True
        return False
