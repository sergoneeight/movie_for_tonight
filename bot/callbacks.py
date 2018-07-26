from enum import Enum


class SearchCallback(Enum):
    POPULAR_MOVIES = '$popular_movies'
    POPULAR_TV_SHOWS = '$popular_tv_shows'
    POPULAR_PEOPLE = '$popular_people'
    TOP_RATED_MOVIES = '$top_rated_movies'
    TOP_RATED_TV_SHOWS = '$top_rated_tv_shows'
    MOVIES_IN_THEATERS = '$movies_in_theaters'


class RandomMovieCallback(Enum):
    NEW_RANDOM_MOVIE = '$new_random_movie'


class GeneralCallback(Enum):
    MORE_LIKE_THIS = '$like'
