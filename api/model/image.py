from enum import Enum


class ImageConfig(object):
    BASE_URL = 'https://image.tmdb.org/t/p/'

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


class Image(object):
    def __init__(self, response_dict):
        self._file_path = response_dict['file_path']
        self._aspect_ratio = response_dict['aspect_ratio']
        self.height = response_dict['height']
        self.width = response_dict['width']
        self.vote_average = response_dict['vote_average']
        self.vote_count = response_dict['vote_count']

    @property
    def url(self):
        return ImageConfig.BASE_URL + ImageConfig.ProfileSize.ORIGINAL.value + self._file_path
