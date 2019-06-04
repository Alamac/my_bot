import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

import handlers
import settings

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

def main():
    mybot = Updater(settings.API_KEY)
    logging.info('Bot starting')

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', handlers.greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler("planet", handlers.define_constellation, pass_user_data=True))
    dp.add_handler(CommandHandler("wordcount", handlers.wordcount, pass_user_data=True))
    dp.add_handler(CommandHandler('next_full_moon', handlers.next_full_moon, pass_user_data=True))
    dp.add_handler(CommandHandler('cities', handlers.cities, pass_user_data=True))
    dp.add_handler(CommandHandler('cat', handlers.send_cat, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать котика)$', handlers.send_cat, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$', handlers.change_avatar, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Инфо)$', handlers.get_info, pass_user_data=True))

    dp.add_handler(MessageHandler(Filters.text, handlers.talk_to_me, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact, handlers.get_contact, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location, handlers.get_location, pass_user_data=True))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
