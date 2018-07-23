import flask
from flask_sslify import SSLify
from telebot import types, TeleBot

import misc
from api.movie_db_service import MovieDbService
from bot.callbacks import PopularMoviesCallback, TheaterMoviesCallback, PopularTVShowsCallback
from bot.carousel import Carousel
from bot.utils import markup_util, inline_query_util

bot = TeleBot(misc.BOT_TOKEN, threaded=False)
app = flask.Flask(__name__)
sslify = SSLify(app)
movie_db_service = MovieDbService()
# Carousels
popular_movies_carousel = Carousel(name='popular_movies')
in_theaters_carousel = Carousel(name='in_theaters')
popular_tv_shows_carousel = Carousel(name='popular_tv_shows')
carousels = set()

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


@bot.message_handler(commands=['popular'])
def send_popular_movies(message):
    movies = movie_db_service.get_popular_movies()
    bot.send_media_group(message.chat.id, media=[], )
    if movies:
        popular_movies_carousel.set_items(movies)
        movie = popular_movies_carousel.current_item
        if movie:
            bot.send_message(
                chat_id=message.chat.id,
                text=movie.caption,
                parse_mode='HTML',
                reply_markup=markup_util.get_carousel_item_markup(
                    item=movie,
                    carousel=popular_movies_carousel,
                    callback=PopularMoviesCallback
                )
            )


@bot.message_handler(commands=['in_theaters'])
def send_in_theaters_movies(message):
    movies = movie_db_service.get_movies_in_theatres()
    if movies:
        in_theaters_carousel.set_items(movies)
        movie = in_theaters_carousel.current_item
        if movie:
            bot.send_message(
                chat_id=message.chat.id,
                text=movie.caption,
                parse_mode='HTML',
                reply_markup=markup_util.get_carousel_item_markup(
                    item=movie,
                    carousel=in_theaters_carousel,
                    callback=TheaterMoviesCallback
                )
            )


@bot.message_handler(commands=['popular_tv_shows'])
def send_popular_tv_shows(message):
    tv_shows = movie_db_service.get_popular_tv_shows()
    if tv_shows:
        popular_tv_shows_carousel.set_items(tv_shows)
        tv_show = popular_tv_shows_carousel.current_item
        if tv_show:
            bot.send_message(
                chat_id=message.chat.id,
                text=tv_show.caption,
                parse_mode='HTML',
                reply_markup=markup_util.get_carousel_item_markup(
                    item=tv_show,
                    carousel=popular_tv_shows_carousel,
                    callback=PopularTVShowsCallback
                )
            )


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
        bot.answer_inline_query(query.id, results=inline_query_util.generate_inline_search_results(search_results),
                                cache_time=10)


# Markup button handlers
@bot.callback_query_handler(func=lambda call: call.data == 'new_random_movie')
def on_retry_random_movie_clicked(call):
    if call.message:
        update_random_movie(chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.inline_message_id:
        update_random_movie(inline_message_id=call.inline_message_id)


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


# @bot.callback_query_handler(func=lambda call: True)
# def on_more_like_this_button_clicked(call):
#     pass
# if PopularMoviesCallback.MORE_LIKE_THIS_BTN.value in call.data:
#     movie_id = call.data.split('-')[1]
#     movie_title = call.data.split('-')[2]
# elif PopularTVShowsCallback.MORE_LIKE_THIS_BTN.value in call.data:
#     tv_show_id = call.data.split('-')[1]
#     tv_show_title = call.data.split('-')[2]
# movie_id = call.data.split('=')[-1]
# send_more_like_this_movie(call.message.chat.id, movie_id)


@bot.callback_query_handler(func=lambda call: True)
def on_next_previous_carousel_buttons_clicked(call):
    if PopularMoviesCallback.NEXT_CAROUSEL_BTN.value in call.data:
        movie = popular_movies_carousel.next()
        __update_carousel(carousel=popular_movies_carousel, item=movie, call=call, callback=PopularMoviesCallback)

    elif PopularMoviesCallback.PREVIOUS_CAROUSEL_BTN.value in call.data:
        movie = popular_movies_carousel.previous()
        __update_carousel(carousel=popular_movies_carousel, item=movie, call=call, callback=PopularMoviesCallback)

    elif TheaterMoviesCallback.NEXT_CAROUSEL_BTN.value in call.data:
        movie = in_theaters_carousel.next()
        __update_carousel(carousel=in_theaters_carousel, item=movie, call=call, callback=TheaterMoviesCallback)

    elif TheaterMoviesCallback.PREVIOUS_CAROUSEL_BTN.value in call.data:
        movie = in_theaters_carousel.previous()
        __update_carousel(carousel=in_theaters_carousel, item=movie, call=call, callback=TheaterMoviesCallback)

    # elif PopularTVShowsCallback.NEXT_CAROUSEL_BTN.value in call.data:
    #     tv_show = popular_tv_shows_carousel.next()
    #     __update_carousel(carousel=popular_tv_shows_carousel, item=tv_show, call=call, callback=PopularTVShowsCallback)
    #
    # elif PopularTVShowsCallback.PREVIOUS_CAROUSEL_BTN.value in call.data:
    #     tv_show = popular_tv_shows_carousel.previous()
    #     __update_carousel(carousel=popular_tv_shows_carousel, item=tv_show, call=call, callback=PopularTVShowsCallback)

    # if PopularMoviesCallback.MORE_LIKE_THIS_BTN.value in call.data:
    #     movies = movie_db_service.get_movie_recommendations()
    #     send_more_like_this(call.message.chat.id, 12, '')
    #
    # elif PopularTVShowsCallback.MORE_LIKE_THIS_BTN.value in call.data:
    #     pass


def __update_carousel(carousel, item, call, callback):
    if item:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=item.caption,
            parse_mode='HTML',
            reply_markup=markup_util.get_carousel_item_markup(
                item=item,
                carousel=carousel,
                callback=callback
            )
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
