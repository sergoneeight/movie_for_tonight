from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.callbacks import SearchCallback, RandomMovieCallback, MarkupButtonCallback
from bot.utils import messages


def get_random_movie_markup(movie):
    markup = InlineKeyboardMarkup()
    details_btn = InlineKeyboardButton(text=messages.DETAILS_BTN_TEXT, url=movie.details_url)
    retry_btn = InlineKeyboardButton(text=messages.RETRY_BTN_TEXT, callback_data=RandomMovieCallback.NEW_RANDOM_MOVIE.value)
    trailer_btn = InlineKeyboardButton(text=messages.VIDEOS_BTN_TEXT, switch_inline_query_current_chat='{callback}-{media_type}-{id}'.format(
        callback=MarkupButtonCallback.VIDEOS.value,
        media_type=movie.media_type,
        id=movie.id,
    ))
    markup.row(details_btn, retry_btn)
    markup.row(trailer_btn)
    markup.row(__recommendations_btn(movie))
    return markup


def __recommendations_btn(search_item):
    query_data = '{callback}-{media_type}-{id}'.format(
        callback=MarkupButtonCallback.RECOMMENDATIONS.value,
        id=search_item.id,
        media_type=search_item.media_type
    )
    return InlineKeyboardButton(
        text=messages.MORE_LIKE_THIS_BTN_TEXT,
        switch_inline_query_current_chat=query_data
    )


def get_inline_popular_markup():
    markup = InlineKeyboardMarkup()
    popular_movies_btn = InlineKeyboardButton(
        text=messages.MOVIES_BTN_TEXT,
        switch_inline_query_current_chat=SearchCallback.POPULAR_MOVIES.value
    )
    popular_tv_shows_btn = InlineKeyboardButton(
        text=messages.TV_SHOWS_BTN_TEXT,
        switch_inline_query_current_chat=SearchCallback.POPULAR_TV_SHOWS.value
    )
    popular_people_button = InlineKeyboardButton(
        text=messages.POPULAR_PEOPLE_BTN_TEXT,
        switch_inline_query_current_chat=SearchCallback.POPULAR_PEOPLE.value
    )
    markup.add(popular_movies_btn)
    markup.add(popular_tv_shows_btn)
    markup.add(popular_people_button)
    return markup


def get_inline_top_rated_markup():
    markup = InlineKeyboardMarkup()
    top_rated_movies_btn = InlineKeyboardButton(
        text=messages.MOVIES_BTN_TEXT,
        switch_inline_query_current_chat=SearchCallback.TOP_RATED_MOVIES.value
    )
    popular_tv_shows_btn = InlineKeyboardButton(
        text=messages.TV_SHOWS_BTN_TEXT,
        switch_inline_query_current_chat=SearchCallback.TOP_RATED_TV_SHOWS.value
    )
    markup.add(top_rated_movies_btn)
    markup.add(popular_tv_shows_btn)
    return markup


def get_single_button_markup(btn_text, callback):
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text=btn_text, switch_inline_query_current_chat=callback.value)
    markup.add(btn)
    return markup


# Search results markups
def get_person_inline_search_result_markup(search_item):
    markup = InlineKeyboardMarkup()
    details_btn = InlineKeyboardButton(text=messages.DETAILS_BTN_TEXT, url=search_item.details_url)
    known_for_btn = InlineKeyboardButton(text=messages.KNOWN_FOR_BTN_TEXT, switch_inline_query_current_chat='{callback}-{person_id}'.format(
        callback=MarkupButtonCallback.KNOWN_FOR.value,
        person_id=search_item.id
    ))
    images_btn = InlineKeyboardButton(text=messages.IMAGES_BTN_TEXT, switch_inline_query_current_chat='{callback}-{person_id}'.format(
        callback=MarkupButtonCallback.IMAGES.value,
        person_id=search_item.id
    ))
    markup.row(details_btn)
    markup.row(known_for_btn)
    # markup.row(images_btn)
    return markup


def get_inline_general_search_result_markup(search_item):
    markup = InlineKeyboardMarkup()
    details_btn = InlineKeyboardButton(text=messages.DETAILS_BTN_TEXT, url=search_item.details_url)
    videos_btn = InlineKeyboardButton(text=messages.VIDEOS_BTN_TEXT, switch_inline_query_current_chat='{callback}-{media_type}-{id}'.format(
        callback=MarkupButtonCallback.VIDEOS.value,
        media_type=search_item.media_type,
        id=search_item.id
    ))
    cast_btn = InlineKeyboardButton(text=messages.CAST_BTN_TEXT, switch_inline_query_current_chat='{callback}-{media_type}-{id}'.format(
        callback=MarkupButtonCallback.CAST.value,
        media_type=search_item.media_type,
        id=search_item.id
    ))
    markup.row(details_btn)
    markup.row(videos_btn)
    markup.row(__recommendations_btn(search_item))
    # markup.row(cast_btn)
    return markup
