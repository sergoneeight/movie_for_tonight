import textwrap

from api.model.genres import Genre
from api.model.image import Image
from api.model.media_type import MediaType
from bot.config import MAX_TITLE_CHARS, MAX_DESCRIPTION_CHARS


class Movie(object):
    BASE_MOVIE_URL = 'https://www.themoviedb.org/movie/'
    POSTER_PLACEHOLDER = 'https://critics.io/img/movies/poster-placeholder.png'

    def __init__(self, response_dict):
        self.id = response_dict['id']
        self._title = response_dict['title']
        self._vote_average = response_dict['vote_average']
        self.vote_count = response_dict['vote_count']
        self.overview = response_dict['overview']
        self.popularity = response_dict['popularity']
        if 'release_date' not in response_dict:
            self.release_date = ''
        else:
            self.release_date = response_dict['release_date']
        self._poster_path = response_dict['poster_path']
        self._backdrop_path = response_dict['backdrop_path']
        self._genre_ids = response_dict['genre_ids']
        self.gold_star = u'\u2B50'
        self.media_type = MediaType.MOVIE.value

    @property
    def caption(self):
        return '<b>{title}</b>\n{genres}\n<b>{rating}</b> {star}<a href="{url}">&#160</a>'.format(
            url=self.details_url,
            title=self.title,
            year=self.release_year,
            genres=self.formatted_genres,
            rating=self.vote_average,
            star=self.gold_star)

    @property
    def description(self):
        return u'{genres}\n{rating} {star}'.format(
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
    def poster_url(self):
        if self._poster_path:
            return Image.BASE_URL + Image.PosterSize.LARGE.value + self._poster_path
        return self.POSTER_PLACEHOLDER

    @property
    def poster_thumb_url(self):
        if self._poster_path:
            return Image.BASE_URL + Image.PosterSize.MEDIUM.value + self._poster_path
        return self.POSTER_PLACEHOLDER

    @property
    def backdrop_url(self):
        if self._backdrop_path:
            return Image.BASE_URL + Image.BackdropSize.MEDIUM.value + self._backdrop_path
        return Image.BASE_URL + Image.PosterSize.MEDIUM.value

    @property
    def details_url(self):
        return self.BASE_MOVIE_URL + str(self.id)

    @property
    def release_year(self):
        return self.release_date.split('-')[0]

    @property
    def genres(self):
        return [Genre.title(genre_id) for genre_id in self._genre_ids]

    @property
    def formatted_genres(self):
        return textwrap.shorten(', '.join(self.genres), MAX_DESCRIPTION_CHARS, placeholder=u'\u2026')

    @property
    def title_with_year(self):
        return self.title + ' ({year})'.format(year=self.release_year)
