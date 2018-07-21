from enum import Enum


class PopularMoviesCallback(Enum):
    NEXT_CAROUSEL_BTN = 'next_popular_movie'
    PREVIOUS_CAROUSEL_BTN = 'previous_popular_movie'


class TheaterMoviesCallback(Enum):
    NEXT_CAROUSEL_BTN = 'next_theater_movie'
    PREVIOUS_CAROUSEL_BTN = 'previous_theater_movie'
