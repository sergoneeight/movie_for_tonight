from enum import Enum


class Video(object):
    BASE_VIDEO_URL = 'https://www.youtube.com/embed/'

    def __init__(self, response_dict):
        self.id = response_dict['id']
        self.type = response_dict['type']
        self.key = response_dict['key']
        self.name = response_dict['name']

    @property
    def url(self):
        return self.BASE_VIDEO_URL + self.key

    @property
    def thumbnail(self):
        return 'https://img.youtube.com/vi/{video_key}/hqdefault.jpg'.format(video_key=self.key)


class VideoType(Enum):
    CLIP = 'Clip'
    TRAILER = 'Trailer'
