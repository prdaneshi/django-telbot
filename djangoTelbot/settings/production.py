from djangoTelbot.settings.base import *
from djangoTelbot.settings.updater_setting import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'deni53okj1kfg0',
        'USER': 'slwywneiwysvah',
        'PASSWORD': '81f78c5ae27dcbbf381e572dfb257b9a41c01c2f3952a3280fad77cb70e7ff59',
        'HOST': 'ec2-54-243-252-232.compute-1.amazonaws.com',
        'PORT': '',
    }
}


try:
    PORT = int(os.environ.get("PORT", "8443"))
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=token)
    updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, token))
except Exception as error:
    print(error)