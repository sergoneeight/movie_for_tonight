from enum import Enum


class SearchCallback(Enum):
    POPULAR_MOVIES = 'popular_movies'
    POPULAR_TV_SHOWS = 'popular_tv_shows'
    POPULAR_PEOPLE = 'popular_people'


class RandomMovieCallback(Enum):
    NEW_RANDOM_MOVIE = 'new_random_movie'


class GeneralCallback(Enum):
    MORE_LIKE_THIS = 'more_like'
