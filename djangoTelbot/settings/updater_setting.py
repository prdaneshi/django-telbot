from telegram.ext import Updater
import os

token = '1168577282:AAF6gv-0KG4ZCiTMykR8X_vW9GLee07g1W8'
#token = os.getenv("TOKEN")
updater = Updater(token, use_context=True)