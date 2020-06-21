from djangoTelbot.settings.base import *
from djangoTelbot.settings.updater_setting import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd3v4uv3vsahuse',
        'USER': 'cznlzubulmcozk',
        'PASSWORD': 'bdabae13c5d64454862ce988fe596b3ada164a73c08c9e591c521dddaf71460e',
        'HOST': 'ec2-54-247-79-178.eu-west-1.compute.amazonaws.com',
        'PORT': '5432',
    }
}


try:
    PORT = int(os.environ.get("PORT", "8443"))
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=token)
    updater.bot.set_webhook("https://{}.herokuapp.com/".format(HEROKU_APP_NAME))
except Exception as error:
    print(error)