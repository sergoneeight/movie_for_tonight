import textwrap
from datetime import datetime

from api.model.genres import Genre
from api.model.image import ImageConfig
from api.model.media_type import MediaType
from bot.config import MAX_DESCRIPTION_CHARS, MAX_TITLE_CHARS


class TVShow(object):
    BASE_TV_SHOW_URL = 'https://www.themoviedb.org/tv/'
    POSTER_PLACEHOLDER = 'https://sergoneeight.pythonanywhere.com/public/media_placeholder.jpg'

    def __init__(self, response_dict):
        self.id = response_dict['id']
        self.title = response_dict['name']
        self.overview = response_dict['overview']
        self._vote_average = response_dict['vote_average']
        self.vote_count = response_dict['vote_count']
        self.popularity = response_dict['popularity']
        self._first_air_date = response_dict['first_air_date'] if 'first_air_date' in response_dict else ''
        self._poster_path = response_dict['poster_path']
        self._backdrop_path = response_dict['backdrop_path']
        self._genre_ids = response_dict['genre_ids']
        self.media_type = MediaType.TV
        self.gold_star = u'\u2B50'

    @property
    def description(self):
        return u'{genres}\n{rating} {star}'.format(
            genres=textwrap.shorten(self.genres_caption, MAX_DESCRIPTION_CHARS, placeholder=u'\u2026'),
            rating=self.vote_average,
            star=self.gold_star)

    @property
    def caption(self):
        return '<b>{title} {year}</b>\n{genres}\n<b>{rating}</b> {star}<a href="{url}">&#160</a>'.format(
            url=self.details_url,
            title=self.title,
            year='({})'.format(self.first_air_date.year) if self.first_air_date else '',
            genres=self.genres_caption,
            rating=self.vote_average,
            star=self.gold_star)

    @property
    def shorten_title(self):
        return textwrap.shorten(self.title, MAX_TITLE_CHARS, placeholder=u'\u2026') + (' ({year})'.format(
            year=self.first_air_date.year) if self.first_air_date else '')

    @property
    def vote_average(self):
        if self._vote_average == 0:
            return 'No ratings'
        return self._vote_average

    @property
    def first_air_date(self):
        date = ''
        try:
            date = datetime.strptime(self._first_air_date, '%Y-%m-%d')
        except ValueError as e:
            print(e)
        finally:
            return date

    @property
    def details_url(self):
        return self.BASE_TV_SHOW_URL + str(self.id)

    @property
    def poster_url(self):
        if self._poster_path:
            return ImageConfig.BASE_URL + ImageConfig.PosterSize.LARGE.value + self._poster_path
        return self.POSTER_PLACEHOLDER

    @property
    def backdrop_url(self):
        return ImageConfig.BASE_URL + ImageConfig.BackdropSize.MEDIUM.value + self._backdrop_path

    @property
    def genres(self):
        return [Genre.title(genre_id) for genre_id in self._genre_ids]

    @property
    def genres_caption(self):
        return ', '.join(self.genres)
