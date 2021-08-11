import logging
import requests
import os

from telegram.ext.filters import InvertedFilter

import config as cfg
from telegram import ParseMode
from telegram.ext import CommandHandler, Defaults, Updater

from recipe_scrapper import get_recetas_gratis, get_cookpad, get_cocineros_argentinos

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def startCommand(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello there!")


def recipeCommand(update, context):
    if len(context.args) > 0:
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
    if len(context.args) > 0:
        response = f"⏳ Buscando recetas relacionadas con los ingredientes informados...\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)

        for param in context.args:
            ingredient = param

            #1
            recipes = []
            recipes = get_recetas_gratis(ingredient)
            response = f"Recetas encontradas en Recetas Gratis:\n"
            context.bot.send_message(chat_id=update.effective_chat.id, text=response)

            for recipe in recipes:
                context.bot.send_message(chat_id=update.effective_chat.id, text=recipe)

            #2
            recipes = []
            recipes = get_cookpad(ingredient)
            response = f"Recetas encontradas en CookPad:\n"
            context.bot.send_message(chat_id=update.effective_chat.id, text=response)

            for recipe in recipes:
                context.bot.send_message(chat_id=update.effective_chat.id, text=recipe)

            #3
            recipes = []
            recipes = get_cocineros_argentinos(ingredient)
            response = f"Recetas encontradas en Cocineros Argentinos:\n"
            context.bot.send_message(chat_id=update.effective_chat.id, text=response)

            for recipe in recipes:
                context.bot.send_message(chat_id=update.effective_chat.id, text=recipe)
    else:
        response = "⚠️ Por favor, ingrese por lo menos un ingrediente para continuar...\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)


if __name__ == "__main__":
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=cfg.TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", startCommand))  # Accessed via /start
    dispatcher.add_handler(CommandHandler("receta", recipeCommand))
    dispatcher.add_handler(CommandHandler("ingredientes", ingredientsCommand))
    
    # log all errors
    dispatcher.add_error_handler(error)
    
    if cfg.MODE == 'webhook':
        # enable webhook
        updater.start_webhook(listen="0.0.0.0",
                            port=int(os.environ.get('PORT', '5000')),
                            url_path=cfg.TELEGRAM_TOKEN,
                            webhook_url=cfg.HEROKU_URL + cfg.TELEGRAM_TOKEN)
    else:
        # enable polling
        updater.start_polling()

    # Wait for the script to be stopped, this will stop the bot as well
    updater.idle()
