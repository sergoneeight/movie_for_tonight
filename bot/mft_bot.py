from telebot import TeleBot

from api.movie_db_service import MovieDbService


class MovieForTonightBot(TeleBot):
    def __init__(self, token):
        super().__init__(token)
        self.movie_db_service = MovieDbService()
        self.popular_movies_response = None


bot = MovieForTonightBot('TOKEN_HERE')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['popular'])
def send_popular_movies(message):
    __request_popular_movies()


@bot.message_handler(commands=['mft'])
def send_random_movie(message):
    movie = bot.movie_db_service.random_movie()
    if movie:
        bot.send_photo(message.chat.id, photo=movie.poster_url, caption=movie.caption)


def __request_popular_movies():
    response = bot.movie_db_service.get_popular_movies_response()
    if response:
        bot.popular_movies_response = response


if __name__ == '__main__':
    bot.polling()
