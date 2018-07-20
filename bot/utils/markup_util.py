from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_random_movie_markup(movie):
    markup = InlineKeyboardMarkup()
    details_btn = InlineKeyboardButton(text='DETAILS', url=movie.details_url)
    retry_btn = InlineKeyboardButton(text=u'RETRY', callback_data='new_random_movie')
    similar_movies_btn = InlineKeyboardButton(
        text='MORE LIKE THAT',
        callback_data='similar_movies_for={movie_id}'.format(movie_id=movie.id)
    )
    markup.row(details_btn, retry_btn)
    markup.row(similar_movies_btn)
    return markup


def get_carousel_item_markup():
    markup = InlineKeyboardMarkup()
    next_btn = InlineKeyboardButton(text=u'NEXT', callback_data='next_item')
    markup.row(next_btn)
    return markup


def get_inline_search_markup():
    markup = InlineKeyboardMarkup()
    switch_button = InlineKeyboardButton(text="SEARCH", switch_inline_query_current_chat='')
    markup.add(switch_button)
    return markup


def get_inline_search_result_markup(search_item):
    markup = InlineKeyboardMarkup()
    details_btn = InlineKeyboardButton(text='DETAILS', url=search_item.details_url)
    markup.row(details_btn)
    return markup
