import flask
from flask_sslify import SSLify
from telebot import types, TeleBot

import misc
from api.movie_db_service import MovieDbService
from bot.callbacks import SearchCallback, RandomMovieCallback
from bot.utils import markup_util, inline_query_util

bot = TeleBot(misc.BOT_TOKEN, threaded=False)
app = flask.Flask(__name__)
sslify = SSLify(app)
movie_db_service = MovieDbService()

# constants
MAX_SIMILAR_MOVIES_RESULTS = 10
TEXT_MESSAGES = {
    'welcome':
        u'Welcome Stranger!\n'
        u'This bot cannot do much right now,\n'
        u'but still you can ask him:\n'
        u'________________________________________\n'
        u'/random_movie - shows random movie\n'
        u'/search - searches for a movie, tv show, person'
}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, text=TEXT_MESSAGES['welcome'])


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


@bot.message_handler(commands=['popular_movies'])
def send_popular_movies(message):
    movies = movie_db_service.get_popular_movies()


@bot.message_handler(commands=['in_theaters'])
def send_in_theaters_movies(message):
    movies = movie_db_service.get_movies_in_theatres()


@bot.message_handler(commands=['popular_tv_shows'])
def send_popular_tv_shows(message):
    tv_shows = movie_db_service.get_popular_tv_shows()


def send_more_like_this(chat_id, id, callback):
    pass
    # movies = movie_db_service.get_similar_movies(movie_id)
    # if movies and len(movies) > 0:
    #     msg = ''
    #     for item_num, movie in enumerate(movies):
    #         if item_num == MAX_SIMILAR_MOVIES_RESULTS:
    #             break
    #         msg += movie.description_with_url
    #
    #     bot.send_message(chat_id, text=msg, parse_mode='HTML', disable_web_page_preview=True)


@bot.message_handler(commands=['search'])
def go_to_inline_search(message):
    bot.send_message(message.chat.id, 'Click the button to start search for a movie, tv show, person',
                     reply_markup=markup_util.get_inline_search_markup())


@bot.message_handler(commands=['popular'])
def go_to_inline_popular_results(message):
    bot.send_message(message.chat.id, 'Select to see currently popular:',
                     reply_markup=markup_util.get_inline_popular_markup())


@bot.inline_handler(func=lambda query: True)
def search_query(query):
    if len(query.query) == 0:
        bot.answer_inline_query(query.id, [], cache_time=0)

    if SearchCallback.POPULAR_MOVIES.value == query.query:
        movies = movie_db_service.get_popular_movies()
        bot.answer_inline_query(query.id, results=inline_query_util.generate_inline_search_results(movies), cache_time=0)

    elif SearchCallback.POPULAR_TV_SHOWS.value == query.query:
        tv_shows = movie_db_service.get_popular_tv_shows()
        bot.answer_inline_query(query.id, results=inline_query_util.generate_inline_search_results(tv_shows), cache_time=0)

    elif SearchCallback.POPULAR_PEOPLE.value == query.query:
        people = movie_db_service.get_popular_people()
        bot.answer_inline_query(query.id, results=inline_query_util.generate_inline_search_results(people), cache_time=0)

    else:
        search_results = movie_db_service.multi_search(query.query)
        bot.answer_inline_query(query.id, results=inline_query_util.generate_inline_search_results(search_results), cache_time=0)


# Markup button handlers
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
