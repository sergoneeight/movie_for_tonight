from enum import Enum

import requests

import misc
from api.model.movie import MoviesResponse
from api.model.tv_show import TVShowsResponse


class MovieDbApi(object):
    API_KEY = misc.MOVIE_DB_API_KEY
    BASE_URL = 'https://api.themoviedb.org/3/'

    class METHOD(Enum):
        POPULAR_MOVIES = 'movie/popular'
        POPULAR_TV_SHOWS = 'tv/popular'

    def _get_endpoint(self, method):
        return self.BASE_URL + method + '?api_key=' + self.API_KEY

    def get_popular_movies(self):
        endpoint = self._get_endpoint(self.METHOD.POPULAR_MOVIES.value)
        http_response = requests.get(endpoint, verify=False)
        if http_response.status_code == 200:
            return MoviesResponse(http_response.json()).get_movies()
        return None

    def get_popular_tv_shows(self):
        endpoint = self._get_endpoint(self.METHOD.POPULAR_TV_SHOWS.value)
        http_response = requests.get(endpoint, verify=False)
        if http_response.status_code == 200:
            return TVShowsResponse(http_response.json()).get_tv_shows()
        return None

    def get_movie(self, movie_id):
        pass

    def get_tv_show(self, tv_show_id):
        pass

    def random_movie(self, filer):
        pass

    def search_movies(self, query):
        pass

    def search_tv_shows(self, query):
        pass
