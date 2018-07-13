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
    def __init__(self, response_dict):
        self.id = response_dict['id']
        self.title = response_dict['title']
        self.vote_average = response_dict['vote_average']
        self.vote_count = response_dict['vote_count']
        self.overview = response_dict['overview']
        self.release_date = response_dict['release_date']
        self._poster_path = response_dict['poster_path']
        self._genre_ids = response_dict['genre_ids']

    @property
    def poster_url(self):
        return Image.BASE_URL + Image.PosterSize.MEDIUM.value + self._poster_path

    @property
    def release_year(self):
        return self.release_date.split('-')[0]

    @property
    def genres(self):
        return [Genre.title(genre_id) for genre_id in self._genre_ids]
