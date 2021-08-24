from __future__ import unicode_literals, absolute_import, division, print_function


class Color(object):
    WHITE = 'white'
    RED = 'red'
    YELLOW = 'yellow'
    BLUE = 'blue'
    GREEN = 'green'
    BLACK = 'black'
    ORANGE = 'orange'
    PURPLE = 'purple'
    PINK = 'pink'
    GRAY = 'gray'
    LIGHT_BLUE = 'light_blue'
    BROWN = 'brown'


COLOR_RU = {
    Color.WHITE: 'Белый',
    Color.RED: 'Красный',
    Color.YELLOW: 'Жёлтый',
    Color.BLUE: 'Синий',
    Color.GREEN: 'Зелёный',
    Color.BLACK: 'Чёрный',
    Color.ORANGE: 'Оранжевый',
    Color.PURPLE: 'Фиолетовый',
    Color.PINK: 'Розовый',
    Color.GRAY: 'Серый',
    Color.LIGHT_BLUE: 'Голубой',
    Color.BROWN: 'Коричневый',
}


COLOR_MIX = [
    {'answer': Color.ORANGE, 'mix':(Color.YELLOW, Color.RED)},
    {'answer': Color.PURPLE, 'mix':(Color.RED, Color.BLUE)},
    {'answer': Color.PINK, 'mix':(Color.RED, Color.WHITE)},
    {'answer': Color.GRAY, 'mix':(Color.WHITE, Color.BLACK)},
    {'answer': Color.GREEN, 'mix':(Color.YELLOW, Color.BLUE)},
    {'answer': Color.LIGHT_BLUE, 'mix':(Color.BLUE, Color.WHITE)},
    {'answer': Color.BROWN, 'mix':(Color.GREEN, Color.RED)},
]
