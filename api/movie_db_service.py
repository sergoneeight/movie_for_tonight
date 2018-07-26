from random import randint

import requests

import misc
from api.model.base_multiple_response import MultipleResponse, ResponseType
from api.model.filter import DiscoverMoviesFilter


class MovieDbService(object):
    API_KEY = misc.MOVIE_DB_API_KEY
    BASE_URL = 'https://api.themoviedb.org/3/'
    BASE_PAYLOAD = {'api_key': API_KEY, 'language': 'en-US'}

    def get_popular_movies(self, page=1):
        endpoint = self.BASE_URL + 'movie/popular'
        payload = self.BASE_PAYLOAD.copy()
        payload.update({'page': str(page)})
        http_response = requests.get(endpoint, params=payload)
        if http_response.status_code == 200:
            return MultipleResponse(http_response.json(), response_type=ResponseType.MOVIE).results
        return None

    def get_top_rated_movies(self, page=1):
        endpoint = self.BASE_URL + 'movie/top_rated'
        payload = self.BASE_PAYLOAD.copy()
        payload.update({'page': str(page)})
        http_response = requests.get(endpoint, params=payload)
        if http_response.status_code == 200:
            return MultipleResponse(http_response.json(), response_type=ResponseType.MOVIE).results
        return None

    def get_popular_tv_shows(self, page=1):
        endpoint = self.BASE_URL + 'tv/popular'
        payload = self.BASE_PAYLOAD.copy()
        payload.update({'page': str(page)})
        http_response = requests.get(endpoint, params=payload)
        if http_response.status_code == 200:
            return MultipleResponse(http_response.json(), response_type=ResponseType.TV_SHOW).results
        return None

    def get_top_rated_tv_shows(self, page=1):
        endpoint = self.BASE_URL + 'tv/top_rated'
        payload = self.BASE_PAYLOAD.copy()
        payload.update({'page': str(page)})
        http_response = requests.get(endpoint, params=payload)
        if http_response.status_code == 200:
            return MultipleResponse(http_response.json(), response_type=ResponseType.TV_SHOW).results
        return None

    def get_popular_people(self, page=1):
        endpoint = self.BASE_URL + 'person/popular'
        payload = self.BASE_PAYLOAD.copy()
        payload.update({'page': str(page)})
        http_response = requests.get(endpoint, params=payload, verify=False)
        if http_response.status_code == 200:
            return MultipleResponse(http_response.json(), response_type=ResponseType.PERSON).results
        return None

    def get_movies_in_theatres(self, page=1):
        endpoint = self.BASE_URL + 'movie/now_playing'
        payload = self.BASE_PAYLOAD.copy()
        payload.update({'region': 'US', 'page': str(page)})
        http_response = requests.get(endpoint, params=payload)
        if http_response.status_code == 200:
            return MultipleResponse(http_response.json(), response_type=ResponseType.MOVIE).results
        return None

    def get_movie_recommendations(self, movie_id, page=1):
        endpoint = self.BASE_URL + 'movie/{movie_id}/recommendations'.format(movie_id=movie_id)
        payload = self.BASE_PAYLOAD.copy()
        payload.update({'page': str(page)})
        http_response = requests.get(endpoint, params=payload)
        if http_response.status_code == 200:
            return MultipleResponse(http_response.json(), response_type=ResponseType.MOVIE).results
        return None

    def get_tv_show_recommendations(self, tv_show_id, page=1):
        endpoint = self.BASE_URL + 'tv/{tv_show_id}/recommendations'.format(tv_show_id=tv_show_id)
        payload = self.BASE_PAYLOAD.copy()
        payload.update({'page': str(page)})
        http_response = requests.get(endpoint, params=payload)
        if http_response.status_code == 200:
            return MultipleResponse(http_response.json(), response_type=ResponseType.TV_SHOW).results
        return None

    def get_random_movie(self):
        max_pages_for_random_choice = 100
        random_page = randint(1, max_pages_for_random_choice)
        endpoint = self.BASE_URL + 'discover/movie'
        payload = self.BASE_PAYLOAD.copy()
        payload.update(DiscoverMoviesFilter(page=random_page).filter)
        http_response = requests.get(endpoint, params=payload)
        if http_response.status_code == 200:
            return MultipleResponse(http_response.json(), response_type=ResponseType.MOVIE).results[randint(1, 19)]
        return None

    def multi_search(self, query, page=1):
        endpoint = self.BASE_URL + 'search/multi'
        payload = self.BASE_PAYLOAD.copy()
        payload.update({'query': str(query), 'page': str(page)})
        http_response = requests.get(endpoint, params=payload)
        if http_response.status_code == 200:
            return MultipleResponse(http_response.json(), response_type=ResponseType.MULTI_SEARCH).results
        return None

    def get_movie_details(self, movie_id):
        pass

    def get_tv_show_details(self, tv_show_id):
        pass
