from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,CallbackContext)
import os
import configparser
import logging
from ChatGPT_HKBU import HKBU_ChatGPT


def main():
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'TELEGRAM_ACCESS_TOKEN' in os.environ:
        config['TELEGRAM']['ACCESS_TOKEN'] = os.environ['TELEGRAM_ACCESS_TOKEN']
    if 'CHATGPT_ACCESS_TOKEN' in os.environ:
        config['CHATGPT']['ACCESS_TOKEN'] = os.environ['CHATGPT_ACCESS_TOKEN']

    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
   
    # You can set this logging module, so you will know when and why things do not work as expected Meanwhile, update your config.ini as:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    # register a dispatcher to handle message: here we register an echo dispatcher
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)

    # dispatcher for chatgpt
    global chatgpt
    chatgpt = HKBU_ChatGPT(config)
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
    dispatcher.add_handler(chatgpt_handler)
    
    # To start the bot:
    updater.start_polling()
    updater.idle()

def equiped_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)
    # Define a few command handlers. These usually take the two arguments update and
    # context. Error handlers also receive the raised TelegramError object in error.

if __name__ == '__main__':
    main()


