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
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['popular'])
def send_popular_movies(message):
    __request_popular_movies()
    # bot.popular_movies = api.get_popular_movies()
    # movies_chunck = get_somth(bot.popular_movies)
    # m = next(movies_chunck)
    #
    # for index, movie in enumerate(m):
    #     click_kb = types.InlineKeyboardMarkup()
    #     click_button = types.InlineKeyboardButton("More Info", callback_data='clicked', url=movie.details_url)
    #     click_kb.row(click_button)
    #     if index == len(m) - 1:
    #         next_btn = types.InlineKeyboardButton("Next movies", callback_data='next_movies')
    #         click_kb.row(next_btn)
    #     bot.send_photo(chat_id=message.chat.id,
    #                    photo=movie.poster_url,
    #                    caption=movie.caption,
    #                    parse_mode='HTML',
    #                    reply_markup=click_kb)


@bot.message_handler(commands=['mft'])
def send_random_movie(message):
    movie = bot.movie_db_service.random_movie()
    if movie:
        markup = types.InlineKeyboardMarkup()
        details_btn = types.InlineKeyboardButton(text='Details', url=movie.details_url)
        markup.row(details_btn)
        bot.send_photo(message.chat.id, photo=movie.poster_url, caption=movie.caption, parse_mode='HTML',
                       reply_markup=markup)


def __request_popular_movies():
    response = bot.movie_db_service.get_popular_movies_response()
    if response:
        bot.popular_movies_response = response


@bot.callback_query_handler(func=lambda call: call.data == 'next_movies')
def on_next_clicked(call):
    bot.send_message(call.message.chat.id, 'On next clicked')


if __name__ == '__main__':
    app.run()
    # bot.polling()
