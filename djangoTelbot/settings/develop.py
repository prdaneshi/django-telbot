from djangoTelbot.settings.base import *
#from djangoTelbot.settings.updater_setting import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'telbotdb',
        'USER': 'postgres',
        'PASSWORD': 'nimamaryammamanbabamankey',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# updater.bot.set_webhook()
# updater.start_polling()
#updater.idle()
ALLOWED_HOSTS = ["*"]