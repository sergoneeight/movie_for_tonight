from enum import Enum


class SearchCallback(Enum):
    POPULAR_MOVIES = '_popular_movies'
    POPULAR_TV_SHOWS = '_popular_tv_shows'
    POPULAR_PEOPLE = '_popular_people'
    TOP_RATED_MOVIES = '_top_rated_movies'
    TOP_RATED_TV_SHOWS = '_top_rated_tv_shows'
    MOVIES_IN_THEATERS = '_in_theaters'
    UPCOMING_MOVIES = '_upcoming_movies'
    TV_ON_THE_AIR = '_on_tv'
    SEARCH = ''


class RandomMovieCallback(Enum):
    NEW_RANDOM_MOVIE = '_new_random_movie'


class MarkupButtonCallback(Enum):
    RECOMMENDATIONS = '_rec'
    VIDEOS = '_vid'
    CAST = '_cast'
    KNOWN_FOR = '_known_for'
    IMAGES = '_img'
