from telegram.ext import Updater
import os


token = os.getenv("TOKEN")
updater = Updater(token, use_context=True)