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


def get_carousel_item_markup(item, current_index, total_items):
    indicator = '{current}|{total}'.format(current=current_index, total=total_items)
    markup = InlineKeyboardMarkup()
    details_btn = InlineKeyboardButton(text='DETAILS', url=item.details_url)
    similar_movies_btn = InlineKeyboardButton(
        text='MORE LIKE THAT',
        callback_data='similar_movies_for={movie_id}'.format(movie_id=item.id)
    )
    next_btn = InlineKeyboardButton(text=u'NEXT', callback_data='next_item')
    previous_btn = InlineKeyboardButton(text=u'PREVIOUS', callback_data='previous_item')
    current_page_indicator = InlineKeyboardButton(text=indicator, callback_data='one')
    markup.row(previous_btn, current_page_indicator, next_btn)
    markup.row(details_btn)
    markup.row(similar_movies_btn)
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
