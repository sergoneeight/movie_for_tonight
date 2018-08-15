from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.callbacks import SearchCallback, RandomMovieCallback, GeneralCallback

MORE_LIKE_THIS_BTN_NAME = u'MORE LIKE THIS'
DETAILS_BTN_NAME = u'DETAILS'
RETRY_BTN_NAME = u'RETRY'
SEARCH_BTN_NAME = u'SEARCH'
NEXT_BTN_NAME = u'NEXT'
PREVIOUS_BTN_NAME = u'PREVIOUS'
MOVIES_BTN_NAME = u'MOVIES'
TV_SHOWS_BTN_NAME = u'TV SHOWS'
POPULAR_PEOPLE_BTN_NAME = u'PEOPLE'
IN_THEATERS_BTN_NAME = u'IN THEATERS'
ON_TV_BUTTON_NAME = u'ON TV'
VIDEOS_BTN_NAME = u'VIDEOS'


def get_random_movie_markup(movie):
    markup = InlineKeyboardMarkup()
    details_btn = InlineKeyboardButton(text=DETAILS_BTN_NAME, url=movie.details_url)
    retry_btn = InlineKeyboardButton(text=RETRY_BTN_NAME, callback_data=RandomMovieCallback.NEW_RANDOM_MOVIE.value)
    trailer_btn = InlineKeyboardButton(text=VIDEOS_BTN_NAME, switch_inline_query_current_chat='{callback}-{media_type}-{id}'.format(
        callback=GeneralCallback.VIDEOS.value,
        media_type=movie.media_type,
        id=movie.id,
    ))
    markup.row(details_btn, retry_btn)
    markup.row(trailer_btn)
    markup.row(__more_like_this_btn(movie))
    return markup


def __more_like_this_btn(search_item):
    query_data = '{callback}-{media_type}-{id}'.format(
        callback=GeneralCallback.MORE_LIKE_THIS.value,
        id=search_item.id,
        media_type=search_item.media_type
    )
    return InlineKeyboardButton(
        text=MORE_LIKE_THIS_BTN_NAME,
        switch_inline_query_current_chat=query_data
    )


def get_inline_search_markup():
    markup = InlineKeyboardMarkup()
    switch_button = InlineKeyboardButton(text=SEARCH_BTN_NAME, switch_inline_query_current_chat='')
    markup.add(switch_button)
    return markup


def get_inline_popular_markup():
    markup = InlineKeyboardMarkup()
    popular_movies_btn = InlineKeyboardButton(
        text=MOVIES_BTN_NAME,
        switch_inline_query_current_chat=SearchCallback.POPULAR_MOVIES.value
    )
    popular_tv_shows_btn = InlineKeyboardButton(
        text=TV_SHOWS_BTN_NAME,
        switch_inline_query_current_chat=SearchCallback.POPULAR_TV_SHOWS.value
    )
    popular_people_button = InlineKeyboardButton(
        text=POPULAR_PEOPLE_BTN_NAME,
        switch_inline_query_current_chat=SearchCallback.POPULAR_PEOPLE.value
    )
    markup.add(popular_movies_btn)
    markup.add(popular_tv_shows_btn)
    markup.add(popular_people_button)
    return markup


def get_inline_top_rated_markup():
    markup = InlineKeyboardMarkup()
    top_rated_movies_btn = InlineKeyboardButton(
        text=MOVIES_BTN_NAME,
        switch_inline_query_current_chat=SearchCallback.TOP_RATED_MOVIES.value
    )
    popular_tv_shows_btn = InlineKeyboardButton(
        text=TV_SHOWS_BTN_NAME,
        switch_inline_query_current_chat=SearchCallback.TOP_RATED_TV_SHOWS.value
    )
    markup.add(top_rated_movies_btn)
    markup.add(popular_tv_shows_btn)
    return markup


def get_inline_in_theaters_markup():
    markup = InlineKeyboardMarkup()
    in_theaters_btn = InlineKeyboardButton(
        text=IN_THEATERS_BTN_NAME,
        switch_inline_query_current_chat=SearchCallback.MOVIES_IN_THEATERS.value
    )
    markup.add(in_theaters_btn)
    return markup


def get_inline_on_tv_markup():
    markup = InlineKeyboardMarkup()
    on_tv_btn = InlineKeyboardButton(
        text=ON_TV_BUTTON_NAME,
        switch_inline_query_current_chat=SearchCallback.TV_ON_THE_AIR.value
    )
    markup.add(on_tv_btn)
    return markup


def get_inline_search_result_markup(search_item):
    markup = InlineKeyboardMarkup()
    details_btn = InlineKeyboardButton(text=DETAILS_BTN_NAME, url=search_item.details_url)
    videos_btn = InlineKeyboardButton(text=VIDEOS_BTN_NAME, switch_inline_query_current_chat='{callback}-{media_type}-{id}'.format(
        callback=GeneralCallback.VIDEOS.value,
        media_type=search_item.media_type,
        id=search_item.id
    ))
    markup.row(details_btn)
    markup.row(videos_btn)
    markup.row(__more_like_this_btn(search_item))
    return markup


def get_person_inline_search_result_markup(search_item):
    markup = InlineKeyboardMarkup()
    details_btn = InlineKeyboardButton(text=DETAILS_BTN_NAME, url=search_item.details_url)
    markup.row(details_btn)
    return markup
