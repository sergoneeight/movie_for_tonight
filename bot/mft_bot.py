import flask
from flask_sslify import SSLify
from telebot import TeleBot, types

import misc
from api.movie_db_service import MovieDbService


class MovieForTonightBot(TeleBot):
    def __init__(self, token):
        super().__init__(token, threaded=False)
        self.movie_db_service = MovieDbService()
        self.popular_movies_response = None


bot = MovieForTonightBot(misc.BOT_TOKEN)
app = flask.Flask(__name__)
sslify = SSLify(app)


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


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, text="""Welcome Stranger!
This bot doеsn't do so much right now,
but still you can ask him:
_______________________________________________________________
/mft - shows random movie""")


@bot.message_handler(commands=['popular'])
def send_popular_movies(message):
    __request_popular_movies()


@bot.message_handler(commands=['mft'])
def send_random_movie(message):
    movie = bot.movie_db_service.random_movie()
    if movie:
        markup = types.InlineKeyboardMarkup()
        details_btn = types.InlineKeyboardButton(text='Details', url=movie.details_url)
        new_movie_btn = types.InlineKeyboardButton(text='Try Again', callback_data='new_movie')
        markup.row(details_btn)
        markup.row(new_movie_btn)
        bot.send_photo(message.chat.id, photo=movie.poster_url, caption=movie.caption, parse_mode='HTML',
                       reply_markup=markup)


def __request_popular_movies():
    response = bot.movie_db_service.get_popular_movies_response()
    if response:
        bot.popular_movies_response = response


@bot.callback_query_handler(func=lambda call: call.data == 'new_movie')
def on_new_random_movie_clicked(call):
    send_random_movie(call.message)


if __name__ == '__main__':
    # app.run()
    bot.polling()
