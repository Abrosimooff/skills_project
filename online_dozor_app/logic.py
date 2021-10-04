from __future__ import unicode_literals, absolute_import, division, print_function

import json
import pickle
import re
from typing import AnyStr, Dict, NoReturn, Optional, List

import requests

from core.utils.misc import SafeContext




# 1. SEND CODE TO PHONE
"""
Request URL: https://api-video.goodline.info/ords/mobile/vc2/auth/phone
Request Method: POST
Status Code: 200 
Remote Address: 212.75.210.181:443
Referrer Policy: strict-origin-when-cross-origin
access-control-allow-credentials: true
access-control-allow-origin: https://video.online-dozor.ru
access-control-expose-headers: Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Credentials, Vary
content-length: 20
content-type: application/json;charset=UTF8
date: Tue, 14 Sep 2021 14:22:41 GMT
vary: Origin
:authority: api-video.goodline.info
:method: POST
:path: /ords/mobile/vc2/auth/phone
:scheme: https
accept: application/json, text/plain, */*, application/json
accept-encoding: gzip, deflate, br
accept-language: ru-RU,ru;q=0.9
api_key: 86e3ff40ec2c52a8504c8669710b4394
content-length: 67
content-type: application/json;charset=UTF-8
origin: https://video.online-dozor.ru
referer: https://video.online-dozor.ru/
sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"
sec-ch-ua-mobile: ?0
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: cross-site
user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
{phone: "79511883897", id_device: "51eba6dcec0a4", id_platform: 3}
id_device: "51eba6dcec0a4"
id_platform: 3
phone: "79511883897"
"""


# 2. SEND CODE FROM SMS
"""
Request URL: https://api-video.goodline.info/ords/mobile/vc2/auth/token/sms
Request Method: POST
Status Code: 200 
Remote Address: 212.75.210.181:443
Referrer Policy: strict-origin-when-cross-origin
access-control-allow-credentials: true
access-control-allow-origin: https://video.online-dozor.ru
access-control-expose-headers: Content-Type, Access-Control-Allow-Origin, Access-Control-Allow-Credentials, Vary
content-length: 758
content-type: application/json;charset=UTF8
date: Tue, 14 Sep 2021 14:23:57 GMT
vary: Origin
:authority: api-video.goodline.info
:method: POST
:path: /ords/mobile/vc2/auth/token/sms
:scheme: https
accept: application/json, text/plain, */*, application/json
accept-encoding: gzip, deflate, br
accept-language: ru-RU,ru;q=0.9
api_key: 86e3ff40ec2c52a8504c8669710b4394
content-length: 37
content-type: application/json;charset=UTF-8
origin: https://video.online-dozor.ru
referer: https://video.online-dozor.ru/
sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"
sec-ch-ua-mobile: ?0
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: cross-site
user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36
{phone: "79511883897", code: "1631"}
code: "1631"
phone: "79511883897"
"""

# SMS RESPONSE

"""
{
"LOGIN":"89511883897"
,"CLIENT_NAME":"89511883897"
,"IS_ADMIN":0
,"REGISTER_DT":"12.09.2018 17:38:18"
,"TOKEN":"CBF6512B-3FE7-7FD4-E053-2965660A6B50"
,"IS_BUGSHAKER_ENABLED":1
,"IS_WIDGET_ENABLED":0
,"IS_PAYED":1
,"ADDRESS":[
{
"ID_ADDRESS":18482
,"CITY":"\u0433. \u041A\u0435\u043C\u0435\u0440\u043E\u0432\u043E"
,"STREET":"\u0443\u043B. \u0414\u0440\u0443\u0436\u0431\u044B"
,"HOUSE":"\u0434. 30\/8"
,"ENTRANCE":"1"
,"FLAT":"\u043A\u0432. 45"
,"CITY_FIAS_GUID":"94bb19a3-c1fa-410b-8651-ac1bf7c050cd"
,"STREET_FIAS_GUID":"135b6a8c-542f-4361-84f2-0fe10a1fc03c"
,"HOUSE_FIAS_GUID":"a82ae846-4f60-4501-92a2-76dc50b2ae31"
,"ENTRANCE_FIAS_GUID":"6E20973F-A4D4-3C22-E053-0100007FEAA2"
,"FLAT_FIAS_GUID":"67355888-2c05-46cf-9d30-92164013cebb"
,"GESTURE":0
}
]
}
"""

PHONE_HEADERS = {
    ':authority': 'api-video.goodline.info',
    ':method': 'POST',
    ':path': '/ords/mobile/vc2/auth/phone',
    ':scheme': 'https',
    'accept': 'application/json, text/plain, */*, application/json',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9',
    'api_key': '86e3ff40ec2c52a8504c8669710b4394',
    'content-length': '67',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://video.online-dozor.ru',
    'referer': 'https://video.online-dozor.ru/',
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
}



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
            phone="79511883897",
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
            phone="79511883897",
            code=code_string,
        )
        response = self.session.post(self.sms_url, data=sms_data)
        if response.status_code == 200:
            response_data = response.json()
            self.auth_info = AuthInfo(response_data)
            self.save_auth_info(self.auth_info)
            return True
        return False
