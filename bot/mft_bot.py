import flask
from flask_sslify import SSLify
from telebot import types, TeleBot

import misc
from api.model.media_type import MediaType
from api.movie_db_service import MovieDbService
from bot.callbacks import SearchCallback, RandomMovieCallback, MarkupButtonsCallback
from bot.utils import markup_util, inline_query_util, messages

bot = TeleBot(misc.BOT_TOKEN, threaded=False)
app = flask.Flask(__name__)
sslify = SSLify(app)
movie_db_service = MovieDbService()


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
        reply_markup=markup_util.get_single_button_markup(btn_text=messages.SEARCH_BTN_TEXT, callback=SearchCallback.SEARCH)
    )


@bot.message_handler(commands=['in_theaters'])
def go_to_inline_in_theaters_results(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.IN_THEATERS_PROMPT,
        reply_markup=markup_util.get_single_button_markup(btn_text=messages.IN_THEATERS_BTN_TEXT, callback=SearchCallback.MOVIES_IN_THEATERS)
    )


@bot.message_handler(commands=['on_tv'])
def go_to_inline_on_tv_results(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=messages.TV_ON_THE_AIR_PROMPT,
        reply_markup=markup_util.get_single_button_markup(btn_text=messages.ON_TV_BUTTON_TEXT, callback=SearchCallback.TV_ON_THE_AIR)
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
    results = []

    if len(query.query) == 0:
        bot.answer_inline_query(query.id, [], cache_time=0)

    if MarkupButtonsCallback.VIDEOS.value in query.query:
        query_data = query.query.split('-')
        item_id = query_data[2]
        media_type = query_data[1]
        if media_type == MediaType.TV_SHOW.value:
            videos = inline_query_util.generate_inline_videos_results(movie_db_service.get_tv_shows_videos(item_id))
        else:
            videos = inline_query_util.generate_inline_videos_results(movie_db_service.get_movie_videos(item_id))
        bot.answer_inline_query(
            inline_query_id=query.id,
            results=videos,
            cache_time=0
        )

    elif MarkupButtonsCallback.MORE_LIKE_THIS.value in query.query:
        query_data = query.query.split('-')
        item_id = query_data[2]
        media_type = query_data[1]
        if MediaType.TV_SHOW.value == media_type:
            results = movie_db_service.get_tv_show_recommendations(tv_show_id=item_id, page=offset)
        else:
            results = movie_db_service.get_movie_recommendations(movie_id=item_id, page=offset)

    elif MarkupButtonsCallback.KNOWN_FOR.value in query.query:
        results = movie_db_service.get_combined_cast(person_id=query.query.split('-')[1])
        # TODO change bot answer here
        bot.answer_inline_query(
            inline_query_id=query.id,
            results=inline_query_util.generate_inline_search_results(results),
            next_offset='',
            cache_time=0,
            is_personal=True
        )

    elif SearchCallback.POPULAR_MOVIES.value == query.query:
        results = movie_db_service.get_popular_movies(page=offset)

    elif SearchCallback.TV_ON_THE_AIR.value == query.query:
        results = movie_db_service.get_tv_on_the_air(page=offset)

    elif SearchCallback.POPULAR_TV_SHOWS.value == query.query:
        results = movie_db_service.get_popular_tv_shows(page=offset)

    elif SearchCallback.POPULAR_PEOPLE.value == query.query:
        results = movie_db_service.get_popular_people(page=offset)

    elif SearchCallback.TOP_RATED_MOVIES.value == query.query:
        results = movie_db_service.get_top_rated_movies(page=offset)

    elif SearchCallback.TOP_RATED_TV_SHOWS.value == query.query:
        results = movie_db_service.get_top_rated_tv_shows(page=offset)

    elif SearchCallback.MOVIES_IN_THEATERS.value == query.query:
        results = movie_db_service.get_movies_in_theatres(page=offset)

    else:
        results = movie_db_service.multi_search(query=query.query, page=offset)

    if results is None:
        results = []

    offset = offset + 1 if len(results) > 0 else ''
    bot.answer_inline_query(
        inline_query_id=query.id,
        results=inline_query_util.generate_inline_search_results(results),
        next_offset=offset,
        cache_time=0,
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
