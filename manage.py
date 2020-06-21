#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    mode = 'local'
    if mode == 'local':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoTelbot.settings.develop')
    elif mode == 'host':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoTelbot.settings.production')
  #  else:
        # raise ImportError(
        #     "WORKTYPE is not set "
        #     "please add WORKTYPE variable in your coding space")


    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    mode = os.getenv("WORKTYPE")
    main()
