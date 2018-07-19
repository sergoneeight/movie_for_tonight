import flask
from flask_sslify import SSLify
from telebot import types, TeleBot

import misc
from api.movie_db_service import MovieDbService
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
        bot.send_photo(
            chat_id=message.chat.id,
            photo=movie.poster_url,
            caption=movie.caption,
            parse_mode='HTML',
            reply_markup=markup_util.get_random_movie_markup(movie)
        )


@bot.message_handler(commands=['popular'])
def send_popular_movies(message):
    # TODO implement "send_popular_movies"
    pass


def send_similar_movies(chat_id, movie_id):
    movies = movie_db_service.get_similar_movies(movie_id)
    if movies and len(movies) > 0:
        msg = ''
        for item_num, movie in enumerate(movies):
            if item_num == MAX_SIMILAR_MOVIES_RESULTS:
                break
            msg += movie.description_with_url

        bot.send_message(chat_id, text=msg, parse_mode='HTML', disable_web_page_preview=True)


@bot.message_handler(commands=["search"])
def go_to_inline_search(message):
    bot.send_message(message.chat.id, "Click the button to start search for a movie, tv show, person",
                     reply_markup=markup_util.get_inline_search_markup())


@bot.inline_handler(func=lambda query: True)
def search_movies_query(query):
    if len(query.query) == 0:
        bot.answer_inline_query(query.id, [], cache_time=0)
    else:
        search_results = movie_db_service.multi_search(query.query)
        bot.answer_inline_query(query.id, results=inline_query_util.generate_inline_search_results(search_results), cache_time=10)


# Markup button handlers
@bot.callback_query_handler(func=lambda call: call.data == 'new_movie')
def on_new_random_movie_clicked(call):
    if call.message:
        send_random_movie(call.message)


@bot.callback_query_handler(func=lambda call: 'similar_movies' in call.data)
def on_similar_movies_clicked(call):
    movie_id = call.data.split('=')[-1]
    send_similar_movies(call.message.chat.id, movie_id)


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
    app.run()
    # bot.polling()
