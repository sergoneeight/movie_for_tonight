from api.model.base_multiple_response import BaseMultipleResponse
from api.model.genres import Genre
from api.model.image import Image


class TVShowsResponse(BaseMultipleResponse):
    def __init__(self, response_dict):
        super().__init__(response_dict)

    def get_tv_shows(self):
        tv_shows = []
        for item in self.results:
            tv_show = TVShow(item)
            tv_shows.append(tv_show)
        return tv_shows


class TVShow(object):
    BASE_TV_SHOW_URL = 'https://www.themoviedb.org/tv/'

    def __init__(self, response_dict):
        self.id = response_dict['id']
        self._title = response_dict['name']
        self.overview = response_dict['overview']
        self.vote_average = response_dict['vote_average']
        self.vote_count = response_dict['vote_count']
        self.first_air_date = response_dict['first_air_date']
        self._poster_path = response_dict['poster_path']
        self._backdrop_path = response_dict['backdrop_path']
        self._genre_ids = response_dict['genre_ids']
        self.gold_star = u'\u2B50'
        self.media_type = 'tv'

    @property
    def description(self):
        return u'{genres}\n{rating} {star}'.format(
            genres=self.formatted_genres,
            rating=self.vote_average,
            star=self.gold_star)

    @property
    def caption(self):
        return '<b>{title}</b> ({year})\n{genres}\n<b>{rating}</b> {star}<a href="{url}">&#160</a>'.format(
            url=self.poster_url,
            title=self.title,
            year=self.first_air_year,
            genres=self.formatted_genres,
            rating=self.vote_average,
            star=self.gold_star)

    @property
    def title(self):
        return self._title + ' ({year})'.format(year=self.release_year)

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
        return ', '.join(self.genres)

    @property
    def release_year(self):
        return self.first_air_date.split('-')[0]

    @property
    def poster_url(self):
        return Image.BASE_URL + Image.PosterSize.MEDIUM.value + self._poster_path

    @property
    def backdrop_url(self):
        return Image.BASE_URL + Image.BackdropSize.MEDIUM.value + self._backdrop_path
