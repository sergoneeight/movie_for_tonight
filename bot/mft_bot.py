import flask
from flask_sslify import SSLify
from telebot import types, TeleBot

import misc
from api.movie_db_service import MovieDbService
from bot.callbacks import SearchCallback, RandomMovieCallback
from bot.utils import markup_util, messages
from bot.utils.inline_results_provider import InlineResultsProvider

bot = TeleBot(misc.BOT_TOKEN, threaded=False)
app = flask.Flask(__name__)
sslify = SSLify(app)
movie_db_service = MovieDbService()
inline_results_provider = InlineResultsProvider(movie_db_service)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, text=messages.WELCOME, parse_mode='HTML', disable_web_page_preview=True)


@bot.message_handler(commands=['random_movie'])
def send_random_movie(message):
    movie = movie_db_service.get_random_movie()
    if movie:
        bot.send_message(
            chat_id=message.chat.id,
            text=movie.caption,
            parse_mode='HTML',
            reply_markup=markup_util.get_random_movie_markup(movie)
        )


@bot.message_handler(commands=['search'])
def go_to_inline_search(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.INLINE_SEARCH_PROMPT,
        reply_markup=markup_util.get_single_button_markup(btn_text=messages.SEARCH_BTN_TEXT,
                                                          callback=SearchCallback.SEARCH)
    )


@bot.message_handler(commands=['in_theaters'])
def go_to_inline_in_theaters_results(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.IN_THEATERS_PROMPT,
        reply_markup=markup_util.get_single_button_markup(btn_text=messages.IN_THEATERS_BTN_TEXT,
                                                          callback=SearchCallback.MOVIES_IN_THEATERS)
    )


@bot.message_handler(commands=['on_tv'])
def go_to_inline_on_tv_results(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.TV_ON_THE_AIR_PROMPT,
        reply_markup=markup_util.get_single_button_markup(btn_text=messages.ON_TV_BUTTON_TEXT,
                                                          callback=SearchCallback.TV_ON_THE_AIR)
    )


@bot.message_handler(commands=['popular'])
def go_to_inline_popular_results(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.POPULAR_PROMPT,
        reply_markup=markup_util.get_inline_popular_markup()
    )


@bot.message_handler(commands=['top_rated'])
def go_to_inline_top_rated_results(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.TOP_RATED_PROMPT,
        reply_markup=markup_util.get_inline_top_rated_markup()
    )


@bot.inline_handler(func=lambda query: True)
def search_query(query):
    offset = int(query.offset) if query.offset else 1
    results = inline_results_provider.get_search_results(query.query, offset)
    offset = offset + 1 if len(results) > 0 else ''
    bot.answer_inline_query(
        inline_query_id=query.id,
        results=results,
        next_offset=offset,
        cache_time=1,
        is_personal=True
    )


@bot.callback_query_handler(func=lambda call: True)
def on_retry_random_movie_clicked(call):
    if RandomMovieCallback.NEW_RANDOM_MOVIE.value == call.data:
        if call.message:
            update_random_movie(chat_id=call.message.chat.id, message_id=call.message.message_id)


def update_random_movie(chat_id=None, message_id=None, inline_message_id=None):
    movie = movie_db_service.get_random_movie()
    if movie:
        bot.edit_message_text(
            text=movie.caption,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            parse_mode='HTML',
            reply_markup=markup_util.get_random_movie_markup(movie)
        )


@app.route('/', methods=['POST', 'GET'])
def index():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
    return '<h1>Hello World</h1>'


if __name__ == '__main__':
    # app.run()
    bot.polling()
