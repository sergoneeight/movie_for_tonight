import textwrap

from api.model.genres import Genre
from api.model.image import Image
from api.model.media_type import MediaType
from bot.config import MAX_TITLE_CHARS, MAX_DESCRIPTION_CHARS


class TVShow(object):
    BASE_TV_SHOW_URL = 'https://www.themoviedb.org/tv/'
    POSTER_PLACEHOLDER = 'https://critics.io/img/movies/poster-placeholder.png'

    def __init__(self, response_dict):
        self.id = response_dict['id']
        self._title = response_dict['name']
        self.overview = response_dict['overview']
        self._vote_average = response_dict['vote_average']
        self.vote_count = response_dict['vote_count']
        self.first_air_date = response_dict['first_air_date']
        self._poster_path = response_dict['poster_path']
        self._backdrop_path = response_dict['backdrop_path']
        self._genre_ids = response_dict['genre_ids']
        self.gold_star = u'\u2B50'
        self.media_type = MediaType.TV_SHOW.value

    @property
    def description(self):
        return u'{genres}\n{rating} {star}'.format(
            genres=self.formatted_genres,
            rating=self.vote_average,
            star=self.gold_star)

    @property
    def caption(self):
        return '<b>{title}</b>\n{genres}\n<b>{rating}</b> {star}<a href="{url}">&#160</a>'.format(
            url=self.details_url,
            title=self.title,
            year=self.first_air_year,
            genres=self.formatted_genres,
            rating=self.vote_average,
            star=self.gold_star)

    @property
    def vote_average(self):
        if self._vote_average == 0:
            return 'No ratings'
        return self._vote_average

    @property
    def title(self):
        return self._title + ' ({year})'.format(year=self.release_year)

    @property
    def formatted_title(self):
        return textwrap.shorten(self._title, MAX_TITLE_CHARS, placeholder=u'\u2026') + ' ({year})'.format(year=self.release_year)

    @property
    def first_air_year(self):
        return self.first_air_date.split('-')[0]

    @property
    def details_url(self):
        return self.BASE_TV_SHOW_URL + str(self.id)

    @property
    def genres(self):
        return [Genre.title(genre_id) for genre_id in self._genre_ids]

    @property
    def formatted_genres(self):
        return textwrap.shorten(', '.join(self.genres), MAX_DESCRIPTION_CHARS, placeholder=u'\u2026')

    @property
    def release_year(self):
        return self.first_air_date.split('-')[0]

    @property
    def poster_url(self):
        if self._poster_path:
            return Image.BASE_URL + Image.PosterSize.LARGE.value + self._poster_path
        return self.POSTER_PLACEHOLDER

    @property
    def backdrop_url(self):
        return Image.BASE_URL + Image.BackdropSize.MEDIUM.value + self._backdrop_path
