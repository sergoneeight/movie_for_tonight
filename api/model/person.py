from api.model.image import Image
from api.model.media_type import MediaType


class Person(object):
    BASE_PERSON_URL = 'https://www.themoviedb.org/person/'
    # TODO change placeholder
    POSTER_PLACEHOLDER = 'https://critics.io/img/movies/poster-placeholder.png'

    def __init__(self, response_dict):
        self.id = response_dict['id']
        self.title = response_dict['name']
        self._profile_path = response_dict['profile_path']
        self._known_for = response_dict['known_for']
        self.media_type = MediaType.PERSON.value

    @property
    def description(self):
        return self.known_for

    @property
    def formatted_title(self):
        return self.title

    @property
    def caption(self):
        return '<b>{name}</b>\n{known_for}<a href="{url}">&#160</a>'.format(
            name=self.title,
            known_for=self.known_for,
            url=self.poster_url
        )

    @property
    def known_for(self):
        return ', '.join([item['title'] if item['media_type'] == MediaType.MOVIE.value else item['name'] for item in self._known_for])

    @property
    def details_url(self):
        return self.BASE_PERSON_URL + str(self.id)

    @property
    def poster_url(self):
        if self._profile_path:
            return Image.BASE_URL + Image.ProfileSize.LARGE.value + self._profile_path
        return self.POSTER_PLACEHOLDER
