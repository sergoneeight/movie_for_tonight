from enum import Enum


class MediaType(Enum):
    MOVIE = 'movie'
    TV = 'tv'
    PERSON = 'person'

    @classmethod
    def from_name(cls, name):
        for media_type in cls:
            if media_type.value == name:
                return media_type
        raise ValueError('"{}" is not valid media type value'.format(name))
