from enum import Enum
from random import randint

import requests

import misc
from api.model.media_type import MediaType
from api.model.response import PagedResponse, VideosResponse, CreditsResponse, ProfileImagesResponse


class MovieDbService(object):
    API_KEY = misc.MOVIE_DB_API_KEY
    BASE_URL = 'https://api.themoviedb.org/3/'

    def get_popular_movies(self, page=1):
        endpoint = self.BASE_URL + 'movie/popular'
        http_response = requests.get(endpoint, params=Payload(page=page))
        if http_response.status_code == 200:
            return PagedResponse(http_response.json(), media_type=MediaType.MOVIE).results
        return None

    def get_top_rated_movies(self, page=1):
        endpoint = self.BASE_URL + 'movie/top_rated'
        http_response = requests.get(endpoint, params=Payload(page=page))
        if http_response.status_code == 200:
            return PagedResponse(http_response.json(), media_type=MediaType.MOVIE).results
        return None

    def get_popular_tv_shows(self, page=1):
        endpoint = self.BASE_URL + 'tv/popular'
        http_response = requests.get(endpoint, params=Payload(page=page))
        if http_response.status_code == 200:
            return PagedResponse(http_response.json(), media_type=MediaType.TV_SHOW).results
        return None

    def get_top_rated_tv_shows(self, page=1):
        endpoint = self.BASE_URL + 'tv/top_rated'
        http_response = requests.get(endpoint, params=Payload(page=page))
        if http_response.status_code == 200:
            return PagedResponse(http_response.json(), media_type=MediaType.TV_SHOW).results
        return None

    def get_tv_on_the_air(self, page=1):
        endpoint = self.BASE_URL + 'tv/on_the_air'
        http_response = requests.get(endpoint, params=Payload(page=page))
        if http_response.status_code == 200:
            return PagedResponse(http_response.json(), media_type=MediaType.TV_SHOW).results
        return None

    def get_popular_people(self, page=1):
        endpoint = self.BASE_URL + 'person/popular'
        http_response = requests.get(endpoint, params=Payload(page=page), verify=False)
        if http_response.status_code == 200:
            return PagedResponse(http_response.json(), media_type=MediaType.PERSON).results
        return None

    def get_movies_in_theatres(self, page=1):
        endpoint = self.BASE_URL + 'movie/now_playing'
        http_response = requests.get(endpoint, params=Payload(page=page, region='US'))
        if http_response.status_code == 200:
            return PagedResponse(http_response.json(), media_type=MediaType.MOVIE).results
        return None

    def get_movie_recommendations(self, movie_id, page=1):
        endpoint = self.BASE_URL + 'movie/{movie_id}/recommendations'.format(movie_id=movie_id)
        http_response = requests.get(endpoint, params=Payload(page=page), verify=False)
        if http_response.status_code == 200:
            return PagedResponse(http_response.json(), media_type=MediaType.MOVIE).results
        return None

    def get_tv_show_recommendations(self, tv_show_id, page=1):
        endpoint = self.BASE_URL + 'tv/{tv_show_id}/recommendations'.format(tv_show_id=tv_show_id)
        http_response = requests.get(endpoint, params=Payload(page=page), verify=False)
        if http_response.status_code == 200:
            return PagedResponse(http_response.json(), media_type=MediaType.TV_SHOW).results
        return None

    def get_random_movie(self):
        max_pages_for_random_choice = 100
        random_page = randint(1, max_pages_for_random_choice)
        endpoint = self.BASE_URL + 'discover/movie'
        http_response = requests.get(endpoint, params=Payload(page=random_page))
        if http_response.status_code == 200:
            return PagedResponse(http_response.json(), media_type=MediaType.MOVIE).results[randint(1, 19)]
        return None

    def multi_search(self, query, page=1):
        endpoint = self.BASE_URL + 'search/multi'
        http_response = requests.get(endpoint, params=Payload(page=page, query=query))
        if http_response.status_code == 200:
            return PagedResponse(http_response.json()).results
        return None

    def discover_movies(self, payload):
        endpoint = self.BASE_URL + 'discover/movie'
        http_response = requests.get(endpoint, params=payload)
        if http_response.status_code == 200:
            return PagedResponse(http_response.json(), media_type=MediaType.MOVIE).results
        return None

    def get_movie_videos(self, movie_id):
        endpoint = self.BASE_URL + 'movie/{movie_id}/videos'.format(movie_id=movie_id)
        http_response = requests.get(endpoint, params=Payload(), verify=False)
        if http_response.status_code == 200:
            return VideosResponse(http_response.json()).videos
        return None

    def get_tv_shows_videos(self, tv_show_id):
        endpoint = self.BASE_URL + 'tv/{tv_id}/videos'.format(tv_id=tv_show_id)
        http_response = requests.get(endpoint, params=Payload(), verify=False)
        if http_response.status_code == 200:
            return VideosResponse(http_response.json()).videos
        return None

    def get_upcoming_movies(self, page=1):
        endpoint = self.BASE_URL + 'movie/upcoming'
        http_response = requests.get(endpoint, params=Payload(page=page))
        if http_response.status_code == 200:
            return PagedResponse(http_response.json(), media_type=MediaType.MOVIE).results
        return None

    def get_combined_cast(self, person_id):
        endpoint = self.BASE_URL + 'person/{person_id}/combined_credits'.format(person_id=person_id)
        http_response = requests.get(endpoint, params=Payload())
        if http_response.status_code == 200:
            return sorted(CreditsResponse(http_response.json()).cast, key=lambda item: item.popularity, reverse=True)
        return None

    def get_movie_credits(self, movie_id):
        endpoint = self.BASE_URL + 'movie/{movie_id}/credits'.format(movie_id=movie_id)
        http_response = requests.get(endpoint, params=Payload())
        if http_response.status_code == 200:
            return CreditsResponse(http_response.json(), MediaType.PERSON).cast
        return None

    def get_tv_credits(self, tv_id):
        endpoint = self.BASE_URL + 'tv/{tv_id}/credits'.format(tv_id=tv_id)
        http_response = requests.get(endpoint, params=Payload())
        if http_response.status_code == 200:
            return CreditsResponse(http_response.json(), MediaType.PERSON).cast
        return None

    def get_person_images(self, person_id):
        endpoint = self.BASE_URL + 'person/{person_id}/images'.format(person_id=person_id)
        http_response = requests.get(endpoint, params=Payload())
        if http_response.status_code == 200:
            return ProfileImagesResponse(http_response.json()).images
        return None

    def discover_tv_shows(self, search_filter):
        pass

    def get_tv_show_details(self, tv_show_id):
        pass


class SortBy(Enum):
    POPULARITY_DESC = 'popularity.desc'
    POPULARITY_ASC = 'popularity.asc'
    VOTE_AVERAGE_DESC = 'vote_average.desc'
    VOTE_AVERAGE_ASC = 'vote_average.asc'


class Payload(dict):

    def __init__(
            self,
            api_key=misc.MOVIE_DB_API_KEY,
            language='en-US',
            region='US',
            sort_by=None,
            page=None,
            release_date_greater_than=None,
            vote_count_greater_than=None,
            vote_average_grater_than=None,
            with_genres=None,
            without_genres=None,
            with_release_type=None,
            query=None,
            primary_release_year=None,
            append_to_response=None,
            primary_release_date_grater_than=None
    ):
        super().__init__()
        self.update({
            'api_key': api_key,
            'language': language,
            'region': region,
            'sort_by': sort_by,
            'page': page,
            'release_date.gte': release_date_greater_than,
            'vote_average.gte': vote_average_grater_than,
            'vote_count.gte': vote_count_greater_than,
            'with_genres': with_genres,
            'without_genres': without_genres,
            'query': query,
            'primary_release_year': primary_release_year,
            'append_to_response': append_to_response,
            'primary_release_date.gte': primary_release_date_grater_than,
            'with_release_type': with_release_type
        })
