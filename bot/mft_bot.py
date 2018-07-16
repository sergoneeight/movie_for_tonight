from telebot import TeleBot

bot = TeleBot('TOKEN_HERE')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(commands=['popular'])
def send_popular_movies(message):
    pass


if __name__ == '__main__':
    bot.polling()
