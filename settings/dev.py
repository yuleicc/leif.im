from .base import *

# DEBUG = False
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'db',
        'PORT': '3306',
    }
}

INSTALLED_APPS += ["debug_toolbar", ]
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

ALLOWED_HOSTS = ['127.0.0.1', 'leif.im']

PAGE_SIZE = 10

SECRET_KEY = "qMiYZLApGklyDu52zr0TobX43dJ9VIgWFvNU7esOB6nacKwhER8tmjSxfQCPH1fM"
