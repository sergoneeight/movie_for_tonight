from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

MORE_LIKE_THIS_BTN_NAME = u'MORE LIKE THIS'
DETAILS_BTN_NAME = u'DETAILS'
RETRY_BTN_NAME = u'RETRY'
SEARCH_BTN_NAME = u'SEARCH'
NEXT_BTN_NAME = u'NEXT'
PREVIOUS_BTN_NAME = u'PREVIOUS'


def get_random_movie_markup(movie):
    markup = InlineKeyboardMarkup()
    details_btn = InlineKeyboardButton(text=DETAILS_BTN_NAME, url=movie.details_url)
    retry_btn = InlineKeyboardButton(text=RETRY_BTN_NAME, callback_data='new_random_movie')
    markup.row(details_btn, retry_btn)
    markup.row(__more_like_this_btn(movie.id))
    return markup


def __more_like_this_btn(item_id):
    return InlineKeyboardButton(
        text=MORE_LIKE_THIS_BTN_NAME,
        callback_data='more_like={item_id}'.format(item_id=item_id)
    )


def get_carousel_item_markup(item, callback, carousel=None):
    page_indicator = '{current}|{total}'.format(current=carousel.current_index + 1, total=carousel.total_items)
    more_like_this_callback = '{callback}-{item_id}-{title}'.format(callback=callback, item_id=item.id)
    markup = InlineKeyboardMarkup()
    details_btn = InlineKeyboardButton(text=DETAILS_BTN_NAME, url=item.details_url)
    more_like_this_btn = InlineKeyboardButton(
        text=MORE_LIKE_THIS_BTN_NAME,
        callback_data='more_like={item_id}'.format(item_id=item.id)
    )
    next_btn = InlineKeyboardButton(text=NEXT_BTN_NAME, callback_data=callback.NEXT_CAROUSEL_BTN.value)
    previous_btn = InlineKeyboardButton(text=PREVIOUS_BTN_NAME, callback_data=callback.PREVIOUS_CAROUSEL_BTN.value)
    current_page_indicator = InlineKeyboardButton(text=page_indicator, callback_data='dummy')
    markup.row(previous_btn, current_page_indicator, next_btn)
    markup.row(details_btn)
    markup.row(more_like_this_btn)
    return markup


def get_inline_search_markup():
    markup = InlineKeyboardMarkup()
    switch_button = InlineKeyboardButton(text=SEARCH_BTN_NAME, switch_inline_query_current_chat='')
    markup.add(switch_button)
    return markup


def get_inline_search_result_markup(search_item):
    markup = InlineKeyboardMarkup()
    details_btn = InlineKeyboardButton(text=DETAILS_BTN_NAME, url=search_item.details_url)
    markup.row(details_btn)
    markup.row(__more_like_this_btn(search_item.id))
    return markup


def get_person_inline_search_result_markup(search_item):
    markup = InlineKeyboardMarkup()
    details_btn = InlineKeyboardButton(text=DETAILS_BTN_NAME, url=search_item.details_url)
    markup.row(details_btn)
    return markup
