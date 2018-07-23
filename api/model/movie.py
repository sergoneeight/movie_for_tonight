from api.model.base_multiple_response import BaseMultipleResponse
from api.model.genres import Genre
from api.model.image import Image


class MoviesResponse(BaseMultipleResponse):
    def __init__(self, response_dict):
        super().__init__(response_dict)

    def get_movies(self):
        movies = []
        for item in self.results:
            movie = Movie(item)
            movies.append(movie)
        return movies


class Movie(object):
    BASE_MOVIE_URL = 'https://www.themoviedb.org/movie/'
    POSTER_PLACEHOLDER = 'https://critics.io/img/movies/poster-placeholder.png'

    def __init__(self, response_dict):
        self.id = response_dict['id']
        self._title = response_dict['title']
        self.vote_average = response_dict['vote_average']
        self.vote_count = response_dict['vote_count']
        self.overview = response_dict['overview']
        self.release_date = response_dict['release_date']
        self._poster_path = response_dict['poster_path']
        self._backdrop_path = response_dict['backdrop_path']
        self._genre_ids = response_dict['genre_ids']
        self.gold_star = u'\u2B50'
        self.media_type = 'movie'

    @property
    def caption(self):
        return '<b>{title}</b> ({year})\n{genres}\n<b>{rating}</b> {star}<a href="{url}">&#160</a>'.format(
            url=self.poster_url,
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
    def description_with_url(self):
        return '<a href="{url}">{movie_title} ({year})</a>'.format(
            url=self.details_url, movie_title=self.title,
            year=self.release_year) + '\n' + self.formatted_genres + '\n' + '<b>{rating}</b>{star}'.format(
            rating=self.vote_average,
            star=self.gold_star) + '\n\n'

    @property
    def title(self):
        return self._title + ' ({year})'.format(year=self.release_year)

    @property
    def poster_url(self):
        if self._poster_path:
            return Image.BASE_URL + Image.PosterSize.LARGE.value + self._poster_path
        return self.POSTER_PLACEHOLDER

    @property
    def poster_thumb_url(self):
        if self._poster_path:
            return Image.BASE_URL + Image.PosterSize.SMALL.value + self._poster_path
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
        return ', '.join(self.genres)

    @property
    def title_with_year(self):
        return self.title + ' ({year})'.format(year=self.release_year)
