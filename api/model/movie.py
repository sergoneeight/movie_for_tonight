from api.model.base_multiple_response import BaseMultipleResponse


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
    IMAGE_BASE_URL = 'http://image.tmdb.org/t/p/w500/'

    def __init__(self, response_dict):
        self.id = response_dict['id']
        self.title = response_dict['title']
        self.vote_average = response_dict['vote_average']
        self.vote_count = response_dict['vote_count']
        self.overview = response_dict['overview']
        self._poster_path = response_dict['poster_path']
        self.release_date = response_dict['release_date']

    @property
    def poster_url(self):
        return self.IMAGE_BASE_URL + self._poster_path

    @property
    def release_year(self):
        return self.release_date.split('-')[0]
