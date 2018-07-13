from enum import Enum


class Image(object):
    BASE_URL = 'http://image.tmdb.org/t/p/'

    class BackdropSize(Enum):
        SMALL = 'w300'
        MEDIUM = 'w780'
        LARGE = 'w1280'
        ORIGINAL = 'original'

    class PosterSize(Enum):
        XXSMALL = 'w92'
        XSMALL = 'w154'
        SMALL = 'w185'
        MEDIUM = 'w342'
        LARGE = 'w500'
        XLARGE = 'w780'
        ORIGINAL = 'original'

    class ProfileSize(Enum):
        SMALL = 'w45'
        MEDIUM = 'w185'
        LARGE = 'h632'
        ORIGINAL = 'original'
