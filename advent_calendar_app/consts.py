# https://advent-kalendari.ru/zadaniya-dlya-advent-kalendarya-dlya-detej/
from typing import AnyStr

from core.wrappers.mrc import Card, CardLink

IMAGE_ID = 457239017  # Константа для карточек 

class Task:
    """ Задание на день """
    text: AnyStr
    text_yesterday: AnyStr
    card: Card

    def __init__(self, text, text_yesterday=None, card=None) -> None:
        self.text = text
        self.text_yesterday = text_yesterday
        self.card = card


TASKS_KIDS = {
    (12, 1): Task('Сделайте дело, которое вы долго откладывали. Пришло время закончить такие дела.'),

    (12, 2): Task(
        text='Напиши себе письмо в будущее, на следующий Новый год, положи его в укромном месте и открой его через год.',
        text_yesterday='Завтра вам предстоит окунуться в будущее.'
    ),

    (12, 3): Task('Составьте с родителями список подарков близким. Наверняка, у вас есть хорошие задумки на этот счёт.',
                  text_yesterday='Завтра подумаем о подарках.'),
    (12, 4): Task(text='Испеки имбирные пряники по рецепту',
                  text_yesterday='Завтра будет что-то вкусненькое.',
                  card=CardLink(url='https://www.youtube.com/watch?v=6mWH0RPbiII',
                                title='Рецепт имбирных пряников',
                                text='Один из варинатов рецептов имбирных пряников. Выбирайте любой',
                                image_id=IMAGE_ID)
                  ),
    (12, 5): Task('Напиши письмо Деду Морозу, и положи его в холодильник, так он точно его получит.',
                  text_yesterday='Для завтрашнего задания понадобится лиcточек и ручка.'),
    (12, 6): Task('Сделай новогоднюю ёлку из ниток по инструкции.',
                  text_yesterday='На завтра нам понадобится большой клубочек ниток.',
                  card=CardLink(url='https://www.youtube.com/watch?v=_t40i0lafQY',
                                title='Ёлочка из ниток',
                                text='Одна из инструкций "Как сделать ёлочку из ниток". Выбирайте любую.',
                                image_id=IMAGE_ID)
                  ),
    (12, 7): Task('Посмотри новогодний мультфильм «Зима в Простоквашино». Разрешается не останавливаться на одном мультфильме.',
                  text_yesterday='Завтра не будет ничего сложного.',
                  card=CardLink(url='https://www.youtube.com/watch?v=gnG9BXeY6fY',
                                title='Трое из простоквашино. Все серии',
                                text='Посмотрите этот или любой другой новогодний мультфильм',
                                image_id=IMAGE_ID)
                  ),
    (12, 8): Task('Сделай кормушку для птичек, или просто возьми еды и накорми их.',
                  text_yesterday='Завтра сделаем одно хорошее дело, а может быть и не одно'),
    (12, 9): Task('Сделай из бумаги гирлянду.', text_yesterday='Завтра займёмся творчеством',
                  card=CardLink(url='https://www.youtube.com/watch?v=8DqzwKrcA-w',
                                title='Гирлянда из снеговиков.',
                                text='Сделайте гирлянду из снеговиков или любую другую бумажную гирлянду.',
                                image_id=IMAGE_ID)
                  ),
    (12, 10): Task('Выучи любой новогодний стих, который тебе понравится.', text_yesterday='Завтра потренеруем память.'),
    (12, 11): Task('Укрась квартиру или дом к Новому году.',
                   text_yesterday='Завтра Вас ждёт приятное семейное задание'),
    (12, 12): Task('Сделай какао с маршмеллоу.', text_yesterday='Завтра будет что-то вкусненькое.',
                   card=CardLink(url='https://www.youtube.com/watch?v=9fACTxDAaKY',
                                 title='Мятное какао с маршмеллоу',
                                 text='Выберите для себя подходящий рецепт какао.',
                                 image_id=IMAGE_ID)
                   ),
    (12, 13): Task('Посмотри со всей семьей ваши старые фотографии или фотографии уходяшего года.',
                   text_yesterday='Завтра вас ждёт ещё одно приятное семейное задание'),
    (12, 14): Task('Посмотри новогодний фильм, например, «Один дома» или «Полярный экспресс» или «Гринч - похититель рождества»',
                   text_yesterday='Для завтрашнего задания нам понадобится свободный вечер.'),
    (12, 15): Task('Вырежи снежинки из бумаги и укрась окна в доме.',
                   text_yesterday='Завтра понадобится бумага «А4», точнее, много бумаги.',
                   card=CardLink(url='https://www.youtube.com/watch?v=4emIrvAKvjw',
                                 title='Снежинки из бумаги',
                                 text='Научитесь вырезать снежинки из бумаги по любой инструкции.',
                                 image_id=IMAGE_ID)),
    (12, 16): Task('Сделай домашнее мороженое по этому рецепту',
                   text_yesterday='Завтра будет что-то вкусненькое.',
                   card=CardLink(url='https://www.youtube.com/watch?v=aWX1YYz8Uaw',
                                 title='Мороженое своими руками',
                                 text='Сделайте вкусное и полезное мороженое своими руками',
                                 image_id=IMAGE_ID)
                   ), #
    (12, 17): Task('Поиграй с семьей или друзьями в настольную игру. А ещё у меня тоже есть интересные игры. '
                   'Можете поиграть со мной',
                   text_yesterday='Завтра будем играть.'),
    (12, 18): Task('Напиши список событий, которые тебя сильно порадовали в этом году.',
                  text_yesterday='Завтра будет много радостных событий.'),
    (12, 19): Task('Собери всю свою семью и вместе нарядите ёлку, если она ещё не наряжена.',
                   text_yesterday='Если у вас ещё нет ёлки, то делаю толстый намёк.'),
    (12, 20): Task('Сходи в гости к родственникам или друзьям.', text_yesterday='Завтра пойдём в гости.'),
    (12, 21): Task('Собери большой пазл с новогодней картиной. А Если такого нет, то попроси у друзей или родителей.', 
                   text_yesterday='Если вы любите собирать пазлы, то завтрашнее задание вам понравится'),
    (12, 22): Task('Сделай семейную фотографию возле ёлки.', text_yesterday='Завтра соберёмся возле ёлочки.'),
    (12, 23): Task('Поиграй в «12 записок». '
                   'Это интересный квест, в котором последовательно спрятано 12 подсказок, которые приведут к призу.', 
                   text_yesterday='Завтра будет интерсная игра',
                   card=CardLink(url='https://sova.today/article/12-zapisok-detskaya-igra/',
                                 title='Правила игры "12 записок"',
                                 text='Если вы ещё не закомы с игрой, '
                                      'то ознакомьтесь с правилами и поиграйте с семьёй или друзьями',
                                 image_id=IMAGE_ID)
                   ),
    (12, 24): Task('Напиши минимум 5 желаний, которые хочешь чтобы исполнились в Новом году. '
                   'Возможно, одно из них, ты загадаешь в новогоднюю ночь.', 
                   text_yesterday='Завтра прийдётся хорошенько подумать, но это пригодится тебе в новогоднюю ночь.'),
    (12, 25): Task('Свари детский глинтвейн', text_yesterday='Завтра пригодятся навыки повара или помощь родителей.',
                   card=CardLink(url='https://www.youtube.com/watch?v=FcWGjhMp6fI',
                                 title='Рецепт десткого глинтвейна',
                                 text='Используйте это трецепт или найдите любой другой.',
                                 image_id=IMAGE_ID)
                   ),
    (12, 26): Task('Слепи новогоднюю поделку из солёного теста.', text_yesterday='Завтра что-то слепим.',
                   card=CardLink(url='https://www.youtube.com/watch?v=5qRQDruyFSc',
                                 title='Лепим из слоёного теста',
                                 text='Не ограничивайте свою фантазию на тему нового года',
                                 image_id=IMAGE_ID)
                   ),
    (12, 27): Task('Сделай горячий шоколад.',
                   text_yesterday='Что-то же такое горячее ждёт нас завтра?',
                   card=CardLink(url='https://www.youtube.com/watch?v=-oSrOxMQzTM',
                                 title='Горячий шоколоад своими руками',
                                 text='Найдите любой рецепт горячего шоколада или используйте этот.',
                                 image_id=IMAGE_ID)
                   ),
    (12, 28): Task('Пускай мыльные пузыри на морозе. Будет интересно! Обещаю',
                   text_yesterday='Завтра ждём морозную погоду, она нам понадобится',
                   card=CardLink(url='https://www.youtube.com/watch?v=VgtR5XEWJZA',
                                 title='Мыльные пузыри на морозе',
                                 text='Посмотрите какие пузыри получаются и попробуйте сами.',
                                 image_id=IMAGE_ID)
                   ),
    (12, 29): Task('Новый год уже очень-очень близко, нужно хорошенько отдохнуть. Покатайся с друзьями на санках или на бублике.',
                   text_yesterday='Новый год уже близко. Нужно хорошенько отдохнуть.'),
    (12, 30): Task('Найди самую большую сосульку.', text_yesterday='Завтра ждёт маленькое, но большое забавное задание.'),
    (12, 31): Task('Поздравляю вас! Уже сегодня пробьют куранты и начнётся новый год! '
                   'Загадай желание в эту новогоднюю ночь. Я желаю, чтобы оно обязательно сбылось. Хороших выходных',
                   text_yesterday='Завтра будете отмечать долгожданный Новый год.'),
}

TASKS_OLDS = {

}

TASK_TEXTS = {
    1: Task('Делай зимние фотки каждый день.'),
    2: Task('Нарисуй ёлку по видео-инструкции.'),
    3: Task('Сделай разные снежинки из цветной бумаги.'),
    4: Task('Напиши список событий, которые тебя сильно порадовали в этом году.'),
    5: Task('Сделай снеговика из подручных материалов.'),
    6: Task('Напиши себе письмо в будущее на следующий Новый год, положи его в укромном месте и открой его через год.',
            text_yesterday='Завтра вам предстоит окунуться в будущее.'),
    7: Task('Сделай семейную фотографию возле ёлки.'),
    8: Task('Напиши минимум 10 своих мечт на Новый год.'),
    9: Task('Нарисуй свою семью возле новогодней ёлки.'),
    10: Task('Сделай открытки своим друзьям и положи им их в почтовый ящик, или если твой друг(подруга) далеко, отправь ему их по почте.'),
    11: Task('Собери ненужные вещи, и отдай их тем кому они нужнее.'),
    12: Task('Сделай наконечник в виде звезды на ёлку'),
    13: Task('Испеки имбирное печенье по рецепту:'),
    14: Task('Напиши письмо Деду Морозу, и положи его в холодильник, так он точно его получит.'),
    15: Task('Сделай новогоднюю ёлку из ниток по инструкции.'),
    16: Task('Посмотри новогодний фильм, например, «Один дома» или «Полярный экспресс» или «Гринч - похититель рождества»'),
    17: Task('Нарисуй узоры на окнах.#'),
    18: Task('Сделай кормушку для птичек, или просто возьми еды и накорми их.'),
    19: Task('Сделай из бумаги гирлянду.'),
    20: Task('Выучи любой новогодний стих.'),
    21: Task('Сходи на улицу погуляй минимум час.'),
    22: Task('Возьми еду, выйди на улицу, покорми бездомных собак и кошек.'),
    23: Task('Укрась квартиру (дом, комнату) к Новому году.'),
    24: Task('Сделай какао с маршмеллоу.'),
    25: Task('Нарисуй Деда Мороза.'),
    26: Task('Узнай про традиции празднования Нового года в других странах.'),
    27: Task('Вырежи ёлку из зелёного картона, укрась её игрушками и повесь её на ёлку.'),
    28: Task('Сделай открытки для своих родителей/бабушек/дедушек.'),
    29: Task('Посмотри со всей семьей ваши старые фотографии или фотографии уходяшего года.'),
    30: Task('Напиши сказку про Новый год.'),
    31: Task('Выполни задания на логику и счет.'),
    32: Task('Сделай новогоднюю ёлку из конфет.'),
    33: Task('Собери в парке шишки и сделай из них новогоднюю игрушку.'),
    34: Task('Сделай веточки дерева заснеженными.'),
    35: Task('Слепи из обычного пластилина Дед Мороза и Снегурочку.'),
    36: Task('Собери всю свою семью и вместе нарядите ёлку.'),
    37: Task('Сделай гирлянду из бусин, пуговиц, или из того что есть у тебя дома.'),
    38: Task('Устрой новогоднюю фотосессию для всей своей семьи, не обязательно иметь хороший фотоаппарат, ты можешь сделать хорошие снимки и на телефон.'),
    39: Task('Слепи снеговика и снегурочку из снега на улице.'),
    40: Task('Возьми мыльные пузыри и дуй их на морозе.'),
    41: Task('Укрась окна в доме снежинками.'),
    42: Task('Сделай домашнее мороженое по этому рецепту:'),
    43: Task('Нарисуй 3 разные снежинки.'),
    44: Task('Сходи на каток.'),
    45: Task('Проведи день с семьей.'),
    46: Task('Полей снег крашеной водой из бутылки.'),
    47: Task('Найди самую большую сосульку.'),
    48: Task('Свари безалкогольный глинтвейн:'),
    49: Task('Спрячь и ищи вместе с семьей игрушки в снегу.'),
    50: Task('Води хороводы вокруг елки на площади.'),
    51: Task('Сделай дерево пожеланий, эти пожелания вы прочитаете в новогоднюю ночь'),
    52: Task('Слепи новогоднюю поделку из солёного теста.'),
    53: Task('Узнай почему в России «Дед Мороз», а зарубежом «Санта Клаус».'),
    54: Task('Сделай снежного ангела.'),
    55: Task('Поиграй с семьей в настольную игру.'),
    56: Task('Сделай дело, которое ты долго откладывал.'),
    57: Task('Сходи в гости к родственникам.'),
    58: Task('Купи мандарины.'),
    59: Task('Выключи вечером дома везде свет и зажги свечи, проведи этот вечер именно при свете свечей.'),
    60: Task('Смени телефонный звонок на новогодний.'),
    61: Task('Прыгни в сугроб.'),
    62: Task('Купи и зажги бенгальские огни.'),
    63: Task('Сделай горячий шоколад.'),
    64: Task('Нарисуй зимний лес.'),
    65: Task('Завари и выпей фруктовый чай.'),
    66: Task('Покатайся на санках.'),
    67: Task('Обсуди с семьей и заведите новогоднюю традицию.'),
    68: Task('Прочитай новую книгу.'),
    69: Task('Укутайся в плед и посмотри фильм «Один дома».'),
    70: Task('Отправься на прогулку в парк, лес, возьми с собой горячий чай и фотоаппарат, сделай зимнии фотографии.'),
    71: Task('Походи по замерзшей луже, послушай треск льда.'),
    72: Task('Сделай перестановку в своей комнате.'),
    73: Task('Собери огромный пазл с новогодней картиной.'),
    74: Task('Купи фигурку с символом Нового года.'),
    75: Task('Устрой пижамную вечеринку со своей семьей.'),
    76: Task('Испеки пирог из мандарин.'),
    78: Task('Загадай желание в новогоднюю ночь.'),
    79: Task('Включи новогодние песни, и слушай их весь день и обязательно подпевай.'),
    80: Task('Сходи в кинотеатр на новогодний фильм или мультфильм.'),
    81: Task('Поиграй в снежки.'),
    82: Task('Научись чему-то новому.'),
    83: Task('Сходи в библиотеку, возьми понравившуюся книгу и читай её вечером.'),
    84: Task('Заведи дневник благодарности, и запиши туда всё за что ты благодарен прошедшему году.'),
    85: Task('Сделай новогодние маски и сделайте всей семьей в них фотосессию.'),
    86: Task('Разбери жесткий диск на компьютере и приведи порядок на рабочем столе.'),
    87: Task('Проведи дома выходные без интернета, компьютера и телефона.'),
    88: Task('Сделай шоколад своими руками.'),
    89: Task('Купи и взорви конфетти.'),
    90: Task('Нарисуй открытку с оленем.'),
    91: Task('Приготовь и наешься оливье. Вам понадобится — картофель вареный (желательно не молодой, а старый) – 4 шт. средних, морковка сваренная — 1 шт., яйца сваренные вкрутую – 4 шт., колбаса вареная «докторская» – 300 г, огурцы маринованные (можно свежие) – 4 шт. средних, горошек зеленый консервированный – 1 банка весом 200 г, майонез – 200-300 г, листья петрушки и укропа по желанию, соль, свежемолотый черный перец.'),
    92: Task('Сделай новогодний венок из мишуры.'),
    93: Task('Испеки домашние синнабоны.'),
    94: Task('Посмотри мультфильм “Хранители снов”.'),
    95: Task('Построй снежную крепость.'),
    96: Task('Попей чай с корицей и медом.'),
    97: Task('Сделай из ткани новогоднюю салфетку для столовых приборов.'),
    98: Task('Напиши для любимого человека на снегу: «Я тебя люблю!».'),
    99: Task('Сделай новогодний венок из мандаринов.'),
    100: Task('Купи шоколадку, сделай упаковку в виде снеговика, и подари ее тому кого любишь.'),
    101: Task('Вырежи новогоднего оленя из бумаги и приклей его на окно.'),
    102: Task('Сделай новогодние игрушки на елку из мандаринов.'),
    103: Task('Приготовь попкорн и посмотри новогодний фильм «Гринч — похититель Рождества».'),
    104: Task('Сделай на дверь снеговика.'),
    105: Task('Научись делать елку из салфеток.'),
    106: Task('Сделай гирлянду из фонариков.'),
    107: Task('Составить с родителями список подарков близким.'),
    108: Task('Написать список своих добрых дел за прошедший год (тоже можно написать «с родителями»).'),
    109: Task('Составить список идей для добрых дел на будущий год.'),
    110: Task('Загадайте необычную загадку, и сделайте не стандартный поиск сюрприза.'),
    111: Task('Посмотреть Новогодний сборник советских мультфильмов на Ютуб.'),
    112: Task('Целый день ходи в пижаме и не заправляй постель.'),
    113: Task('Попроси прощение у всех кого обидел в уходящем году.'),
    114: Task('Отправь поздравления своим старым друзьям с кем ты давно не общался.'),
    115: Task('Узнай какие имена в разных странах у Деда Мороза.'),
    116: Task('Почитай новогодние сказки, такие как: «Морозко», «Снежная королева», «Щелкунчик и мышиный король».'),
    117: Task('Устрой домашний кукольный театр или театр теней.'),
    118: Task('Сделай новогоднюю мягкую игрушку ручной работы.'),
    119: Task('Поиграй в «12 записок». Это интересный квест, в котором последовательно спрятано 12 подсказок, которые приведут к призу.'),
    120: Task('Поиграй в игру «Крокодил». Суть игры в том, что человек должен отгадать слово, которое написано на стикере на лбу или отгадать слово по описанию, а также можно загадывать слово и показывать его ничего не говоря.'),
    121: Task('Сходи в театр на новогоднюю пьесу.'),
    122: Task('Поиграй в игру «Фанты». Нужно написать на бумажках разные действия и положить их в шапку, а затем вытягивать и выполнять задания.'),
    123: Task('Попробуй новые хобби.'),
    124: Task('Сделай мыло или свечу в новогоднем стиле.'),
    125: Task('Напиши список дел для саморазвития в новом году.'),
    126: Task('Сделай «Ананас» из бутылки детского шампанского и конфет.'),
    127: Task('Научись делать маскарадную маску.'),
    128: Task('Сделай домашнюю бомбочку для ванны.'),
    129: Task('Подготовь новогодние конкурсы.'),
    130: Task('Сделай шары из ниток.'),
    131: Task('Наладь отношения с теми, с кем были в ссоре.'),
    132: Task('Сделай самодельную хлопушку.'),
    133: Task('Сделай ёлочку из мандаринов.'),
    134: Task('Сделай самодельный подсвечник.'),
    135: Task('Сделай 3D-открытку со снежинкой.'),
    136: Task('Сделай новогоднюю закладку для книги.'),
    137: Task('Сделай гирлянду из вязаных помпонов.'),
    138: Task('Сделай венок из бумаги.'),
    139: Task('Сделай пингвинов из бутылок.'),
    140: Task('Сделай самодельный скраб и устрой вечер красоты.'),
    141: Task('Сделай снежинки из пластиковых бутылок.'),
    142: Task('Сделай семейное дерево.'),
    143: Task('Попробуй ручную роспись одежды.'),
    144: Task('Поиграйте с семьёй в угадай слово.'),
    145: Task('Напиши минимум 5 желаний, которые хочешь чтобы исполнились в Новом году.'),
    146: Task('Посмотри новогодний мультфильм «Зима в Простоквашино». Разрешается не останавливаться на одном мультфильме.')
}


TOMORROW_PHRASES = [
    'Намекнуть какое задание будет завтра?',
    'Намекнуть о задании на завтра?',
    'Дать намёк о задании на завтра?',

    'Подсказать какое задание ждёт вас завтра?',
    'Подсказать какое задание будет завтра?',
    'Подсказать о задании на завтра?',

    'Рассказать какое задание ждёт вас завтра?',
    'Рассказать какое задание будет завтра?',
    'Рассказать о задании на завтра?',
]

TOMORROW_ANSWERS = [
    'да',
    'намекн',
    'расска',
    'подска'
]