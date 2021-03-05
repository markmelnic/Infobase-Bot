from infobase import *

import logging
import configparser as cfg
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

CONFIG_FILE = "config.cfg"
CFG = cfg.RawConfigParser()
CFG.read(CONFIG_FILE)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
LOGGER = logging.getLogger(__name__)

INQUIRY = {}
START, ENTITY, SEARCH, RESULT = range(4)

def start(update: Update, context: CallbackContext) -> None:
    reply_keyboard = [['Person', 'Company', 'Address', 'IDNO']]
    update.message.reply_text(
        'Hi! I investigate infobase.md and return all the data for a person you are researching.\n\nFirst, select the type of entity you are looking for.',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return START

def entity(update: Update, context: CallbackContext) -> None:
    INQUIRY['rtype'] = update.message.text
    LOGGER.info("[USER: %s] - [Entity Type: %s]" % (update.message.from_user.username, INQUIRY['rtype']))

    update.message.reply_text(
        'Nice! Insert the %s.' % INQUIRY['rtype'].lower(),
    )
    return ENTITY

def search(update: Update, context: CallbackContext) -> None:
    INQUIRY['entity'] = update.message.text
    LOGGER.info("[USER: %s] - [Entity keyword(s): %s]" % (update.message.from_user.username, INQUIRY['entity']))

    update.message.reply_text('Searching, please wait...')

    explorer = Explorer(INQUIRY['entity'])
    update.message.reply_text('Found, here is the data %s' % explorer.results)
    return SEARCH

def cancel(update: Update, context: CallbackContext) -> int:
    LOGGER.info("[USER: %s] - [CANCELED]" % (update.message.from_user.username, INQUIRY['entity']))

    update.message.reply_text('Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Help!')

def main():
    updater = Updater(CFG.get("credentials", "token"))
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            START: [MessageHandler(Filters.update, entity)],
            ENTITY: [MessageHandler(Filters.update, search)],
            SEARCH: [MessageHandler(Filters.update, start)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("help", help))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()