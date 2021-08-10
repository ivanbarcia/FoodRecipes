import logging
import requests
import os

import config as cfg
from telegram import ParseMode
from telegram.ext import CommandHandler, Defaults, Updater

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

# extract chat_id based on the incoming object
def get_chat_id(update, context):
    chat_id = -1

    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]

    return chat_id


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def startCommand(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello there!")


def recipeCommand(update, context):
    if len(context.args) > 1:
        response = f"⏳ Buscando recetas relacionadas con los ingredientes informados...\n"
        # crypto = context.args[0].upper()
        # sign = context.args[1]
        # price = context.args[2]

        # context.job_queue.run_repeating(
        #     priceAlertCallback,
        #     interval=15,
        #     first=15,
        #     context=[crypto, sign, price, update.message.chat_id],
        # )

        # response = f"⏳ I will send you a message when the price of {crypto} reaches ${price}, \n"
        # response += f"the current price of {crypto} is ${client.get_symbol_ticker(symbol = crypto + 'USDT')['price']}"
    else:
        response = "⚠️ Por favor, ingrese por lo menos un ingrediente para continuar...\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


def ingredientsCommand(update, context):
    if len(context.args) > 1:
        response = f"⏳ Buscando recetas relacionadas con los ingredientes informados...\n"
        # crypto = context.args[0].upper()
        # sign = context.args[1]
        # price = context.args[2]

        # context.job_queue.run_repeating(
        #     priceAlertCallback,
        #     interval=15,
        #     first=15,
        #     context=[crypto, sign, price, update.message.chat_id],
        # )

        # response = f"⏳ I will send you a message when the price of {crypto} reaches ${price}, \n"
        # response += f"the current price of {crypto} is ${client.get_symbol_ticker(symbol = crypto + 'USDT')['price']}"
    else:
        response = "⚠️ Por favor, ingrese por lo menos un ingrediente para continuar...\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=response)


if __name__ == "__main__":
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=cfg.TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", startCommand))  # Accessed via /start
    dispatcher.add_handler(CommandHandler("receta", recipeCommand))
    dispatcher.add_handler(CommandHandler("ingredientes", ingredientsCommand))
    
    # log all errors
    dispatcher.add_error_handler(error)

    # Start the bot
    # updater.start_polling()
    updater.start_webhook(
        listen="0.0.0.0",
        port=int(cfg.PORT),
        url_path=cfg.TELEGRAM_TOKEN,
        webhook_url=cfg.HEROKU_URL + cfg.TELEGRAM_TOKEN,
    )

    # Wait for the script to be stopped, this will stop the bot as well
    updater.idle()
