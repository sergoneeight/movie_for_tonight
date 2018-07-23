from enum import Enum

from api.model.base_multiple_response import BaseMultipleResponse
from api.model.genres import Genre
from api.model.image import Image


class MultiSearchResponse(BaseMultipleResponse):
    def __init__(self, response_dict):
        super().__init__(response_dict)

    def get_search_items(self):
        search_items = []
        for item in self.results:
            search_item = MultiSearchItem(item)
            search_items.append(search_item)
        return search_items


class MultiSearchItem(object):
    BASE_MOVIE_URL = 'https://www.themoviedb.org/movie/'
    BASE_TV_SHOW_URL = 'https://www.themoviedb.org/tv/'
    BASE_PERSON_URL = 'https://www.themoviedb.org/person/'
    POSTER_PLACEHOLDER = 'https://critics.io/img/movies/poster-placeholder.png'

    class MediaType(Enum):
        MOVIE = 'movie'
        TV_SHOW = 'tv'
        PERSON = 'person'

    def __init__(self, response_dict):
        self.media_type = response_dict['media_type']
        self.id = response_dict['id']
        self.gold_star = u'\u2B50'

        if self.media_type == self.MediaType.MOVIE.value:
            self._title = response_dict['title']
            self._poster_path = response_dict['poster_path']
            self._release_date = response_dict['release_date']
            self._genre_ids = response_dict['genre_ids']
            self._vote_average = response_dict['vote_average']

        elif self.media_type == self.MediaType.TV_SHOW.value:
            self._title = response_dict['name']
            self._poster_path = response_dict['poster_path']
            self._release_date = response_dict['first_air_date']
            self._genre_ids = response_dict['genre_ids']
            self._vote_average = response_dict['vote_average']

        elif self.media_type == self.MediaType.PERSON.value:
            self._title = response_dict['name']
            self._poster_path = response_dict['profile_path']

    @property
    def title(self):
        if self.media_type == self.MediaType.MOVIE.value or self.media_type == self.MediaType.TV_SHOW.value:
            return self._title + ' ({year})'.format(year=self.__get_release_year())
        elif self.media_type == self.MediaType.PERSON.value:
            return self._title
        return ''

    @property
    def description(self):
        if self.media_type == self.MediaType.MOVIE.value or self.media_type == self.MediaType.TV_SHOW.value:
            description = u'{genres}\n{rating} {star}'.format(
                genres=self.__get_formatted_genres(),
                rating=self._vote_average,
                star=self.gold_star)
            return description
        elif self.media_type == self.MediaType.PERSON.value:
            return 'Actor'
        return ''

    @property
    def caption(self):
        if self.media_type == self.MediaType.MOVIE.value or self.media_type == self.MediaType.TV_SHOW.value:
            caption = '<b>{title}</b>\n{genres}\n<b>{rating}</b> {star}<a href="{url}">&#160</a>'.format(
                url=self.poster_url,
                title=self.title,
                genres=self.__get_formatted_genres(),
                rating=self._vote_average,
                star=self.gold_star)
            return caption

        elif self.media_type == self.MediaType.PERSON.value:
            return '<b>{title}</b>\n{type}<a href="{url}">&#160</a>'.format(
                title=self.title,
                type=self.media_type.capitalize(),
                url=self.poster_url
            )
        return ''

    @property
    def poster_url(self):
        if self._poster_path:
            if self.media_type == self.MediaType.PERSON.value:
                return Image.BASE_URL + Image.ProfileSize.LARGE.value + self._poster_path
            return Image.BASE_URL + Image.PosterSize.LARGE.value + self._poster_path
        return self.POSTER_PLACEHOLDER

    @property
    def details_url(self):
        if self.media_type == self.MediaType.MOVIE.value:
            return self.BASE_MOVIE_URL + str(self.id)
        elif self.media_type == self.MediaType.TV_SHOW.value:
            return self.BASE_TV_SHOW_URL + str(self.id)
        elif self.media_type == self.MediaType.PERSON.value:
            return self.BASE_PERSON_URL + str(self.id)
        return ''

    def __get_genres(self):
        return [Genre.title(genre_id) for genre_id in self._genre_ids]

    def __get_formatted_genres(self):
        return ', '.join(self.__get_genres())

    def __get_release_year(self):
        return self._release_date.split('-')[0]
