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
        self._new_movie_btn = types.InlineKeyboardButton(text=u'Retry', callback_data='new_movie')
        self.text_messages = {
            'welcome':
                u'Welcome Stranger!\n'
                u'This bot cannot do much right now,\n'
                u'but still you can ask him:\n'
                u'________________________________________\n'
                u'/mft - shows random movie'
        }

    def get_random_movie_markup(self, movie):
        random_movie_markup = types.InlineKeyboardMarkup()
        details_btn = types.InlineKeyboardButton(text='Details', url=movie.details_url)
        similar_movies_btn = types.InlineKeyboardButton(text='Similar Movies',
                                                        callback_data='similar_movies_for={movie_id}'.format(movie_id=movie.id))
        random_movie_markup.row(details_btn, self._new_movie_btn)
        random_movie_markup.row(similar_movies_btn)
        return random_movie_markup


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
    bot.send_message(message.chat.id, text=bot.text_messages['welcome'])


@bot.message_handler(commands=['popular'])
def send_popular_movies(message):
    __request_popular_movies()


@bot.message_handler(commands=['mft'])
def send_random_movie(message):
    movie = bot.movie_db_service.random_movie()
    if movie:
        bot.send_photo(chat_id=message.chat.id, photo=movie.poster_url, caption=movie.caption,
                       parse_mode='HTML', reply_markup=bot.get_random_movie_markup(movie))


def send_similar_movies(chat_id, movie_id):
    movies = bot.movie_db_service.get_similar_movies(movie_id)
    msg = ''
    for item, movie in enumerate(movies):
        if item == 10:
            break
        msg += '<a href="{url}">{movie_title} ({year})</a>'.format(
            url=movie.details_url, movie_title=movie.title,
            year=movie.release_year) + '\n' + movie.formatted_genres + '\n' + '<b>{rating}</b>{star}'.format(
            rating=movie.vote_average,
            star=movie._gold_star) + '\n\n'

        # msg += movie.caption + '\n' + '<a href="{url}">{movie_title}</a>'.format(url=movie.poster_url, movie_title=movie.title) + '\n\n'
    # bot.send_photo(chat_id=chat_id, photo=movie.poster_url, caption=movie.caption,
    #                parse_mode='HTML', reply_markup=bot.get_random_movie_markup(movie))

    bot.send_message(chat_id, text=msg, parse_mode='HTML', disable_web_page_preview=True)


def __request_popular_movies():
    response = bot.movie_db_service.get_popular_movies_response()
    if response:
        bot.popular_movies_response = response


@bot.inline_handler(func=lambda query: True)
def similar_movies_query(query):
    if len(query.query) == 0:
        bot.answer_inline_query(query.id, [], cache_time=0)
    else:
        movies = bot.movie_db_service.search_movies(query.query)
        results = []
        if movies:
            for item_num, movie in enumerate(movies):
                if item_num == 20:
                    break
                item = types.InlineQueryResultArticle(
                    id=item_num,
                    title=movie.title,
                    description=movie.caption,
                    input_message_content=types.InputTextMessageContent(
                        message_text=movie.caption + '<a href="{url}">.</a>'.format(url=movie.details_url),
                        parse_mode='HTML',
                    ),
                    thumb_url=movie.poster_url
                )
                results.append(item)
        bot.answer_inline_query(query.id, results, cache_time=10)


# Markup button handlers
@bot.callback_query_handler(func=lambda call: call.data == 'new_movie')
def on_new_random_movie_clicked(call):
    send_random_movie(call.message)


@bot.callback_query_handler(func=lambda call: 'similar_movies' in call.data)
def on_similar_movies_clicked(call):
    movie_id = call.data.split('=')[-1]
    send_similar_movies(call.message.chat.id, movie_id)


if __name__ == '__main__':
    # app.run()
    bot.polling()
