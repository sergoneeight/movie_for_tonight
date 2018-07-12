from telebot import TeleBot
from movie_db_api import get_popular_movies

TOKEN = '595208354:AAHKafsVTLRt2xYJDOeoNzhlADcXCI00UGA'

bot = TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['popular'])
def send_popular_movies(message):
    movies = get_popular_movies().get_movies()
    black_star = '&#9733'
    gold_star = '&#11088'
    mes = u'<a href="{poster_url}">&#160</a>\n<b>{title}</b> ({year})\n<b>{rating}</b> {star}'.format(
        poster_url=movies[7].poster_url,
        title=movies[7].title,
        rating=movies[7].vote_average,
        year=movies[7].release_year,
        star=gold_star
    )
    bot.send_message(message.chat.id, mes, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling()
