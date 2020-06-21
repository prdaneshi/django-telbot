from django.apps import AppConfig
from djangoTelbot.settings.updater_setting import *
from telegram.ext import CommandHandler
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


TELEGRAM_URL = "https://api.telegram.org/bot"
TOKEN = os.getenv("TOKEN", "error_token")

class BotConfig(AppConfig):
    name = 'bot'

def help(update, context):
    update.message.reply_text('/help '
                              '/start '
                              '/connect '
                              '/deleteTb '
                              '/close '
                              '/createTb ')

logger.info("Loading handlers for telegram bot")
help_command = CommandHandler('help', help)
updater.dispatcher.add_handler(help_command)
updater.dispatcher.add_error_handler(error)
updater.bot.set_webhook()
updater.start_polling()
