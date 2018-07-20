import flask
from flask_sslify import SSLify
from telebot import types, TeleBot

import misc
from api.movie_db_service import MovieDbService
from bot.carousel import Carousel
from bot.utils import markup_util, inline_query_util

bot = TeleBot(misc.BOT_TOKEN, threaded=False)
app = flask.Flask(__name__)
sslify = SSLify(app)
movie_db_service = MovieDbService()
popular_movies_carousel = Carousel()
popular_movies = None

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
            text=movie.caption2,
            parse_mode='HTML',
            reply_markup=markup_util.get_random_movie_markup(movie)
        )


@bot.message_handler(commands=['popular'])
def send_popular_movies(message):
    movies = movie_db_service.get_popular_movies()
    if movies:
        popular_movies_carousel.set_items(movies)
        movie = popular_movies_carousel.current_item
        if movie:
            bot.send_message(
                chat_id=message.chat.id,
                text='<b>Here is most popular movies:</b>\n\n' + movie.caption2,
                parse_mode='HTML',
                reply_markup=markup_util.get_carousel_item_markup(movie, popular_movies_carousel.current_index, popular_movies_carousel.total_items)
            )


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
@bot.callback_query_handler(func=lambda call: call.data == 'new_random_movie')
def on_new_random_movie_clicked(call):
    if call.message:
        update_random_movie(call.message)


def update_random_movie(message):
    movie = movie_db_service.get_random_movie()
    if movie:
        bot.edit_message_text(
            text=movie.caption2,
            chat_id=message.chat.id,
            message_id=message.message_id,
            parse_mode='HTML',
            reply_markup=markup_util.get_random_movie_markup(movie)
        )


@bot.callback_query_handler(func=lambda call: 'similar_movies' in call.data)
def on_similar_movies_clicked(call):
    movie_id = call.data.split('=')[-1]
    send_similar_movies(call.message.chat.id, movie_id)


@bot.callback_query_handler(func=lambda call: True)
def on_next_previous_carousel_buttons_clicked(call):
    if 'next_item' in call.data:
        movie = popular_movies_carousel.next()
        if movie:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='<b>Here is most popular movies:</b>\n\n' + movie.caption2,
                parse_mode='HTML',
                reply_markup=markup_util.get_carousel_item_markup(movie, popular_movies_carousel.current_index, popular_movies_carousel.total_items)
            )
    elif 'previous_item' in call.data:
        movie = popular_movies_carousel.previous()
        if movie:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text='<b>Here is most popular movies:</b>\n\n' + movie.caption2,
                parse_mode='HTML',
                reply_markup=markup_util.get_carousel_item_markup(movie, popular_movies_carousel.current_index, popular_movies_carousel.total_items)
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
    app.run()
    # bot.polling()
