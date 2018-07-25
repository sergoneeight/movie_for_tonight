from api.model.base_multiple_response import BaseMultipleResponse
from api.model.image import Image


class PersonsResponse(BaseMultipleResponse):
    def __init__(self, response_dict):
        super().__init__(response_dict)

    def get_persons(self):
        persons = []
        for item in self.results:
            person = Person(item)
            persons.append(person)
        return persons


class Person(object):
    BASE_PERSON_URL = 'https://www.themoviedb.org/person/'
    # TODO change placeholder
    POSTER_PLACEHOLDER = 'https://critics.io/img/movies/poster-placeholder.png'

    def __init__(self, response_dict):
        self.id = response_dict['id']
        self.title = response_dict['name']
        self._profile_path = response_dict['profile_path']
        self.media_type = 'person'

    @property
    def description(self):
        return self.media_type.capitalize()

    @property
    def formatted_title(self):
        return self.title

    @property
    def caption(self):
        return '<b>{name}</b>\n{type}<a href="{url}">&#160</a>'.format(
            name=self.title,
            type=self.media_type.capitalize(),
            url=self.poster_url
        )

    @property
    def details_url(self):
        return self.BASE_PERSON_URL + str(self.id)

    @property
    def poster_url(self):
        if self._profile_path:
            return Image.BASE_URL + Image.ProfileSize.LARGE.value + self._profile_path
        return self.POSTER_PLACEHOLDER
