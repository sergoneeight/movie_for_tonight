from random import randint

import requests

import misc
from api.model.filter import DiscoverMoviesFilter
from api.model.movie import MoviesResponse
from api.model.tv_show import TVShowsResponse


class MovieDbService(object):
    API_KEY = misc.MOVIE_DB_API_KEY
    BASE_URL = 'https://api.themoviedb.org/3/'
    BASE_PAYLOAD = {'api_key': API_KEY, 'language': 'en-US'}

    def get_popular_movies_response(self):
        endpoint = self.BASE_URL + 'movie/popular'
        http_response = requests.get(endpoint, params=self.BASE_PAYLOAD, verify=False)
        if http_response.status_code == 200:
            return MoviesResponse(http_response.json())
        return None

    def get_similar_movies(self, movie_id):
        endpoint = self.BASE_URL + 'movie/{movie_id}/recommendations'.format(movie_id=movie_id)
        http_response = requests.get(endpoint, params=self.BASE_PAYLOAD, verify=False)
        if http_response.status_code == 200:
            return MoviesResponse(http_response.json()).get_movies()
        return None

    def get_popular_tv_shows(self):
        endpoint = self.BASE_URL + 'tv/popular'
        http_response = requests.get(endpoint, params=self.BASE_PAYLOAD, verify=False)
        if http_response.status_code == 200:
            return TVShowsResponse(http_response.json()).get_tv_shows()
        return None

    def get_movies_in_theatres(self):
        endpoint = self.BASE_URL + 'movie/now_playing'
        payload = self.BASE_PAYLOAD.copy()
        payload.update({'region': 'US'})
        http_response = requests.get(endpoint, params=payload, verify=False)
        pass

    def get_movie(self, movie_id):
        pass

    def get_tv_show(self, tv_show_id):
        pass

    def random_movie(self):
        max_pages_for_random_choice = 100
        random_page = randint(1, max_pages_for_random_choice)
        endpoint = self.BASE_URL + 'discover/movie'
        payload = self.BASE_PAYLOAD.copy()
        payload.update(DiscoverMoviesFilter(page=random_page).filter)
        http_response = requests.get(endpoint, params=payload)
        if http_response.status_code == 200:
            return MoviesResponse(http_response.json()).get_movies()[randint(1, 19)]
        return None

    def search_movies(self, query):
        endpoint = self.BASE_URL + 'search/movie'
        payload = self.BASE_PAYLOAD.copy()
        payload.update({'query': str(query)})
        http_response = requests.get(endpoint, params=payload, verify=False)
        if http_response.status_code == 200:
            return MoviesResponse(http_response.json()).get_movies()
        return None

    def search_tv_shows(self, query):
        pass
