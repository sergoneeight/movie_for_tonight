import textwrap
from datetime import datetime

from api.model.genres import Genre
from api.model.image import ImageConfig
from api.model.media_type import MediaType
from bot.config import MAX_TITLE_CHARS, MAX_DESCRIPTION_CHARS


class Movie(object):
    BASE_MOVIE_URL = 'https://www.themoviedb.org/movie/'
    POSTER_PLACEHOLDER = 'https://sergoneeight.pythonanywhere.com/public/media_placeholder.jpg'

    def __init__(self, response_dict):
        self.id = response_dict['id']
        self.title = response_dict['title']
        self._vote_average = response_dict['vote_average']
        self.vote_count = response_dict['vote_count']
        self.overview = response_dict['overview']
        self.popularity = response_dict['popularity']
        self._release_date = response_dict['release_date'] if 'release_date' in response_dict else ''
        self._poster_path = response_dict['poster_path']
        self._backdrop_path = response_dict['backdrop_path']
        self._genre_ids = response_dict['genre_ids']
        self.media_type = MediaType.MOVIE
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
            year='({})'.format(self.release_date.year) if self.release_date else '',
            genres=self.genres_caption,
            rating=self.vote_average,
            star=self.gold_star)

    @property
    def shorten_title(self):
        return textwrap.shorten(self.title, MAX_TITLE_CHARS, placeholder=u'\u2026') + (' ({year})'.format(
            year=self.release_date.year) if self.release_date else '')

    @property
    def vote_average(self):
        if self._vote_average == 0:
            return 'No ratings'
        return self._vote_average

    @property
    def release_date(self):
        date = ''
        try:
            date = datetime.strptime(self._release_date, '%Y-%m-%d')
        except ValueError as e:
            print(e)
        finally:
            return date

    @property
    def poster_url(self):
        if self._poster_path:
            return ImageConfig.BASE_URL + ImageConfig.PosterSize.LARGE.value + self._poster_path
        return self.POSTER_PLACEHOLDER

    @property
    def poster_thumb_url(self):
        if self._poster_path:
            return ImageConfig.BASE_URL + ImageConfig.PosterSize.MEDIUM.value + self._poster_path
        return self.POSTER_PLACEHOLDER

    @property
    def backdrop_url(self):
        if self._backdrop_path:
            return ImageConfig.BASE_URL + ImageConfig.BackdropSize.MEDIUM.value + self._backdrop_path
        return ImageConfig.BASE_URL + ImageConfig.PosterSize.MEDIUM.value

    @property
    def details_url(self):
        return self.BASE_MOVIE_URL + str(self.id)

    @property
    def genres(self):
        return [Genre.title(genre_id) for genre_id in self._genre_ids]

    @property
    def genres_caption(self):
        return ', '.join(self.genres)
