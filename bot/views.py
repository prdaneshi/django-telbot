from django.http import HttpResponse
from djangoTelbot.settings.updater_setting import *
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import psycopg2
import logging
import os

from bot import models
from django.core.exceptions import ObjectDoesNotExist

# logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


REQUEST_KWARGS = {
    'proxy_url': 'socks5://127.0.0.1:9050',
}

mode = os.getenv("WORKTYPE")
token = os.getenv("TOKEN")
global conn, cur
conn = None

# updater = Updater(token, use_context=True)
'''
If we use use_context=True in Updater, we should pass arguments to the function this way:
def greet_user(`update: Update, context: CallbackContext`):
    update.message.reply_text('hello')
'''


def run(updater):
    if mode == 'local':
        updater.bot.set_webhook()
        updater.start_polling()
    elif mode == 'host':
        try:
            PORT = int(os.environ.get("PORT", "8443"))
            HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
            updater.start_webhook(listen="0.0.0.0",
                                  port=PORT,
                                  url_path=token)
            updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, token))
        except Exception as error:
            print(error)
            logger.error(error)
    else:
        logger.error("Mode is has not een set")


# ------------------------------------------------------------------


def close(update, context):
    global conn
    if conn is not None:
        conn.close()
        conn = None
        print("Connection Closed")
        update.message.reply_text('connection closed')
    else:
        print("Already closed")
        update.message.reply_text("Already closed")


# -----------------------------------------------------------------


def createTb(update, context):
    try:
        cur.execute(''' 
    CREATE TABLE public."user"(
    id serial,
    name "char",
    birth smallint,
    city "char",
    gender boolean,
    chatId integer,
    PRIMARY KEY (id) );
    ''')
        print("database created")
    except(Exception, psycopg2.DatabaseError) as error:
        cur.execute("ROLLBACK;")
        print(error)


def connect(update, context):
    global conn, cur
    if not conn:
        if mode == 'local':
            try:
                print("Connecting to local Database")
                conn = psycopg2.connect(host="localhost", database="telbotdb", user="telbot", password="telbotpass")
                cur = conn.cursor()
                print("Local database Connected")
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
        elif mode == 'host':
            try:
                print("Connecting to host Database")
                conn = psycopg2.connect(host="ec2-54-243-252-232.compute-1.amazonaws.com",
                                        database="deni53okj1kfg0",
                                        user="slwywneiwysvah",
                                        password="81f78c5ae27dcbbf381e572dfb257b9a41c01c2f3952a3280fad77cb70e7ff59")
                cur = conn.cursor()
                print("Host database connected")
            except(Exception, psycopg2.DatabaseError) as error:
                print(error)
                update.message.reply_text(error)
        else:
            logger.error("Mode has not been set")
            update.message.reply_text("Mode has not been set")
    else:
        print("Database has connected")
        update.message.reply_text("Database has connected")

    cur.execute('SELECT version()')
    db_version = cur.fetchone()
    update.message.reply_text(str(db_version) + '/close')


def deleteTb(update, context):
    global cur
    try:
        cur.execute("DROP TABLE public.user")
        print("DATABASE deleted")
        update.message.reply_text("DATABASE deleted")
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        update.message.reply_text(str(error))
        cur.execute("ROLLBACK;")
    db_version = cur.fetchone()


def start(update, context):
    try:
        if models.Profile.objects.get(chatId=update.effective_user.id):
            keyboard = [
                [InlineKeyboardButton("Next", callback_data=2)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text("{} welcome back to our bot.\n"
                                      "press next if u want to join us".format(update.message.chat.first_name),
                                      reply_markup=reply_markup)
            return 0

    except ObjectDoesNotExist:
        keyboard = [
            [InlineKeyboardButton("Next", callback_data=1)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text("{} welcome to our bot.\n"
                                  "press next if u want to join us".format(update.message.chat.first_name),
                                  reply_markup=reply_markup)
        return 0


def first(update, context):
            if update.callback_query:
                query = update.callback_query
                if update.callback_query.data == '1':
                    query.edit_message_text(text="Good Choice")
                    try:
                        p = models.Profile.objects.create(name=update.message.chat.first_name,
                                                          chatId=update.message.chat.id)
                        keyboard = [
                            [InlineKeyboardButton("Next", callback_data=3)]
                        ]
                        reply_markup = InlineKeyboardMarkup(keyboard)
                        query.bot.sendMessage(chat_id=query.message.chat.id,
                                              text="Now send me your birth year\n"
                                                   "and press next",
                                              reply_markup=reply_markup)
                        # return 1
                    except:
                        query.bot.sendMessage(chat_id=query.message.chat.id,
                                              text="Your name didn't saved.")

                elif update.callback_query.data == '2':
                    query.edit_message_text(text="Nice to meet u")
                    try:
                        p = models.Profile.objects.filter(chatId=query.message.chat.id,
                                                   birth__isnull=False)
                        if p:
                            query.bot.sendMessage(chat_id=query.message.chat.id,
                                                  text="Good, We have your birth too")
                            return second(update, context)#???????????????????????????????????????????????
                        else:
                            keyboard = [
                                [InlineKeyboardButton("Next", callback_data=3)]
                            ]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            query.bot.sendMessage(chat_id=query.message.chat.id,
                                                  text="{} it seems u dont entered your birth year.\n"
                                                       "send me your birth year and then \n"
                                                       "press next".format(query.message.chat.first_name),
                                                  reply_markup=reply_markup)
                    except:
                        query.bot.sendMessage(chat_id=query.message.chat.id,
                                              text="something went wrong")

                elif update.callback_query.data == '3':
                    if models.Profile.objects.filter(chatId=query.message.chat.id,
                                                   birth__isnull=False):
                        return second(update, context)

            elif update.message:
                try:
                    if int(update.message.text) > 1300:
                        p = models.Profile.objects.filter(chatId=update.message.chat.id) \
                            .update(birth=update.message.text)
                        if p:
                            update.message.reply_text("Your birth saved!! :/")
                            return 1
                        #  return second(update, context)
                except(Exception) as error:
                    print(error)
                    update.message.reply_text(str(error))
                    update.message.reply_text("Ahmagh!! :/")
            else:
                update.message.reply_text("Wrong answer, please send me your birth year")
    # except:
    #     update.bot.sendMessage(chat_id=update.message.chat.id,
    #                           text="error1")


def second(update, context):
    if update.callback_query:
        query = update.callback_query
        if update.callback_query.data == '3':
            query.edit_message_text(text="very goood")
            try:
                keyboard = [
                    [InlineKeyboardButton("Next", callback_data=4)]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.bot.sendMessage(chat_id=query.message.chat.id,
                                      text="Now send me your city year\n"
                                           "and press next",
                                      reply_markup=reply_markup)
            except:
                query.bot.sendMessage(chat_id=query.message.chat.id,
                                      text="Your name didn't saved.")
                return 1

        elif update.callback_query.data == '2':
            query.edit_message_text(text="second def")
            try:
                p = models.Profile.objects.filter(chatId=query.message.chat.id,
                                              birth__isnull=False,
                                                  city__isnull=False)


                if p:
                    query.bot.sendMessage(chat_id=query.message.chat.id,
                                          text="Good, We have your city too")
                    return third(update, context)
                else:

                    keyboard = [
                        [InlineKeyboardButton("Next", callback_data=4)]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    query.bot.sendMessage(chat_id=query.message.chat.id,
                                          text="{} it seems u dont entered your city year.\n"
                                               "send me your city and then \n"
                                               "press next".format(query.message.chat.first_name),
                                          reply_markup=reply_markup)
                    return 1
            except:
                query.bot.sendMessage(chat_id=query.message.chat.id,
                                      text="something went wrong")

        elif update.callback_query.data == '4':
            if models.Profile.objects.filter(chatId=query.message.chat.id,
                                              birth__isnull=False,
                                                  city__isnull=False):
                return third(update, context)
    elif update.message:
        try:
            #   if int(lastupdate.message.text) > 1300:
            p = models.Profile.objects.filter(chatId=update.message.chat.id) \
                .update(city=update.message.text)
            if p:
                update.message.reply_text("Your city saved!! :/")
        except(Exception) as error:
            print(error)
            update.message.reply_text(str(error))
            update.message.reply_text("????!! :/")
            #return 1
    else:
        update.message.reply_text("Wrong answer, please send me your birth year")


def third(update, context):
    if update.callback_query:
        query = update.callback_query
        if update.callback_query.data == '4':
            query.edit_message_text(text="nice jooob")
            try:
                keyboard = [
                    [InlineKeyboardButton("Male", callback_data='t'),
                     InlineKeyboardButton("Female", callback_data='f')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                query.bot.sendMessage(chat_id=query.message.chat.id,
                                      text="Now what is your gender",
                                      reply_markup=reply_markup)
                return 2
            except:
                query.bot.sendMessage(chat_id=query.message.chat.id,
                                      text="Your name didn't saved.")

        elif update.callback_query.data == '2':
            query.edit_message_text(text="third def")
            try:
                p = models.Profile.objects.filter(chatId=query.message.chat.id,
                                                  birth__isnull=False,
                                                  city__isnull=False,
                                                  gender__isnull=False)
                if p:
                    query.bot.sendMessage(chat_id=query.message.chat.id,
                                          text="Good, We have your gender too")
                    return fourth(update, context)
                else:

                    keyboard = [
                        [InlineKeyboardButton("Male", callback_data='t'),
                         InlineKeyboardButton("Female", callback_data='f')]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    query.bot.sendMessage(chat_id=query.message.chat.id,
                                          text="{} it seems u dont entered your gender.\n"
                                               "what is your gender? \n".format(query.message.chat.first_name),
                                          reply_markup=reply_markup)
                    return 2
            except:
                query.bot.sendMessage(chat_id=query.message.chat.id,
                                      text="error 5")

        elif update.callback_query.data == 't':
            try:
                models.Profile.objects.filter(chatId=query.message.chat.id) \
                    .update(gender=update.callback_query.data)
                return fourth(update, context)
            except:
                query.bot.sendMessage(chat_id=query.message.chat.id,
                                      text="error t")

        elif update.callback_query.data == 'f':
            try:
                models.Profile.objects.filter(chatId=query.message.chat.id) \
                    .update(gender=update.callback_query.data)
                return fourth(update, context)
            except:
                query.bot.sendMessage(chat_id=query.message.chat.id,
                                      text="error f")
    else:
        update.message.reply_text("Wrong answer, please send me your birth year")


def fourth(update, context):
    try:
        update.callback_query.edit_message_text(text="fourth def")
        update.callback_query.bot.sendMessage(chat_id=update.callback_query.message.chat.id,
                              text="finished")
    except:
        update.callback_query.bot.sendMessage(chat_id=update.message.chat.id,
                              text="error4")


def help(update, context):
    update.message.reply_text('/help '
                              '/start '
                              '/connect '
                              '/deleteTb '
                              '/close '
                              '/createTb ')


def main(request):
    try:
        run(updater)
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start)],
            states={
                0: [CallbackQueryHandler(first), MessageHandler(Filters.all, first)],
                1: [CallbackQueryHandler(second), MessageHandler(Filters.all, second)],
                2: [CallbackQueryHandler(third), MessageHandler(Filters.all, third)]
            },
            fallbacks=[CommandHandler('start', start)]
        )

        help_command = CommandHandler('help', help)
        # start_command = CommandHandler('start', start)
        delete_command = CommandHandler('deleteTb', deleteTb)
        connect_command = CommandHandler('connect', connect)
        finish_command = CommandHandler('close', close)
        create_command = CommandHandler('createTb', createTb)

        updater.dispatcher.add_handler(delete_command)
        updater.dispatcher.add_handler(help_command)
        # updater.dispatcher.add_handler(start_command)
        updater.dispatcher.add_handler(connect_command)
        updater.dispatcher.add_handler(finish_command)
        updater.dispatcher.add_handler(create_command)

        updater.dispatcher.add_error_handler(error)
        updater.dispatcher.add_handler(conv_handler)

        updater.idle()
        return HttpResponse("Bot Started")
    except Exception as er:
        print(er)
        return HttpResponse("Somting went wrong")
