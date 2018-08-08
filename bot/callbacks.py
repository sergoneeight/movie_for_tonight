from enum import Enum


class SearchCallback(Enum):
    POPULAR_MOVIES = '_popular_movies'
    POPULAR_TV_SHOWS = '_popular_tv_shows'
    POPULAR_PEOPLE = '_popular_people'
    TOP_RATED_MOVIES = '_top_rated_movies'
    TOP_RATED_TV_SHOWS = '_top_rated_tv_shows'
    MOVIES_IN_THEATERS = '_movies_in_theaters'


class RandomMovieCallback(Enum):
    NEW_RANDOM_MOVIE = '_new_random_movie'


class GeneralCallback(Enum):
    MORE_LIKE_THIS = '_like'
    VIDEOS = '_vid'
