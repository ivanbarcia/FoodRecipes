import logging
import os
import config as cfg
import time

from telegram.ext import CommandHandler, Updater
from telegram.chataction import ChatAction

from recipe_scrapper import get_recetas_gratis, get_cookpad, get_cocineros_argentinos

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def helpCommand(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Hola!\nPara poder buscar una receta solo basta con tipear los ingredientes o receta que estan buscando y les va a mostrar las distintas opciones que se encuentren\nEjemplo: /receta tomate cebolla\n/receta lemonpie\n")


def recipeCommand(update, context):
    if len(context.args) > 0:
        ingredients = " ".join(context.args)
    
        response = f"⏳ Buscando recetas relacionadas con los ingredientes <b>{ingredients}</b>...\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode="HTML")

        #1
        recipes = []
        recipes = get_recetas_gratis(ingredients)
        if recipes:
            response = f"💡 Recetas encontradas en <b>Recetas Gratis</b>:\n"
            context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode="HTML")

            # Typing
            context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING, timeout=1)
            time.sleep(1)

            for recipe in recipes:
                context.bot.send_message(chat_id=update.effective_chat.id, text=recipe)

        #2
        recipes = []
        recipes = get_cookpad(ingredients)
        if recipes:
            response = f"💡 Recetas encontradas en <b>CookPad</b>:\n"
            context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode="HTML")

            # Typing
            context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING, timeout=1)
            time.sleep(1)

            for recipe in recipes:
                context.bot.send_message(chat_id=update.effective_chat.id, text=recipe)

        #3
        recipes = []
        recipes = get_cocineros_argentinos(ingredients)
        if recipes:
            response = f"💡 Recetas encontradas en <b>Cocineros Argentinos</b>:\n"
            context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode="HTML")

            # Typing
            context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING, timeout=1)
            time.sleep(1)

            for recipe in recipes:
                context.bot.send_message(chat_id=update.effective_chat.id, text=recipe)
    else:
        response = "⚠️ Por favor, ingrese por lo menos un ingrediente para continuar...\nEjemplo: /recetas tomate cebolla ajo \n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=response)


if __name__ == "__main__":
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token=cfg.TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("help", helpCommand))  # Accessed via /help
    dispatcher.add_handler(CommandHandler("receta", recipeCommand))
    
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
