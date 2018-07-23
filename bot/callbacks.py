from enum import Enum


class PopularMoviesCallback(Enum):
    NEXT_CAROUSEL_BTN = 'next_popular_movie'
    PREVIOUS_CAROUSEL_BTN = 'previous_popular_movie'
    MORE_LIKE_THIS_BTN = 'more_like_this_movie'


class TheaterMoviesCallback(Enum):
    NEXT_CAROUSEL_BTN = 'next_theater_movie'
    PREVIOUS_CAROUSEL_BTN = 'previous_theater_movie'
    MORE_LIKE_THIS_BTN = 'more_like_this_movie'


class PopularTVShowsCallback(Enum):
    NEXT_CAROUSEL_BTN = 'next_popular_tv_show'
    PREVIOUS_CAROUSEL_BTN = 'previous_popular_tv_show'
    MORE_LIKE_THIS_BTN = 'more_like_this_tv_show'
