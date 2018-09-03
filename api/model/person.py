from api.model.image import ImageConfig
from api.model.media_type import MediaType


class Person(object):
    BASE_PERSON_URL = 'https://www.themoviedb.org/person/'
    POSTER_PLACEHOLDER = 'http://www.irdconline.com/wp-content/uploads/2018/05/person-placeholder.jpg'

    def __init__(self, response_dict):
        self.id = response_dict['id']
        self.name = response_dict['name']
        self._profile_path = response_dict['profile_path']
        self._known_for = response_dict['known_for'] if 'known_for' in response_dict else []
        self.character = response_dict['character'] if 'character' in response_dict else ''
        self.media_type = MediaType.PERSON

    @property
    def description(self):
        if self.character:
            return self.character
        return self.known_for

    @property
    def caption(self):
        return '<b>{name}</b>\n{known_for}<a href="{url}">&#160</a>'.format(
            name=self.name,
            known_for=self.known_for if self.known_for else self.character,
            url=self.poster_url
        )

    @property
    def shorten_title(self):
        return self.name

    @property
    def known_for(self):
        return ', '.join([item['title'] if item['media_type'] == MediaType.MOVIE.value else item['name'] for item in self._known_for])

    @property
    def details_url(self):
        return self.BASE_PERSON_URL + str(self.id)

    @property
    def poster_url(self):
        if self._profile_path:
            return ImageConfig.BASE_URL + ImageConfig.ProfileSize.LARGE.value + self._profile_path
        return self.POSTER_PLACEHOLDER
