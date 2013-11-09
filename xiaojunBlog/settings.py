# Django settings for xiaojunBlog project.
#coding=utf8
from platform import  platform
from os import path
if 'Ubuntu' in platform():
    print'..............................ubuntu, 本来是false'
    DEBUG=True
else:
    print'..............................not ubuntu'+platform()
    DEBUG=False

TEMPLATE_DEBUG = DEBUG

ROOT_PATH = path.abspath(path.join(path.dirname('settings.py'),path.pardir))

ADMINS = (
    ('weirdbird', '1016728789@qq.com'),
)


print("----------------------------------------------------setting0")
MANAGERS = ADMINS

if DEBUG:
    DOMAIN ="http://localhost:8000"
    DB_NAME = 'xiaojunBlog'
    DB_USER = 'root'
    DB_PWD = 'mysql'
else:
    DOMAIN ="weirdbird.net"
    DB_NAME = 'xiaojunBlog'
    DB_USER = 'root'
    DB_PWD = 'mysql'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'xiaojunBlog',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'root',
        'PASSWORD': 'mysql',
        'HOST': '127.0.0.1',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '3306',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['localhost','weirdbird.net']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
# STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    path.join(ROOT_PATH,'xiaojunBlog/static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'pt$=2p-5k+sr1z2m$yej)2u%7p!=f^494m9&efeh!1-&m2#2w_'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

print("----------------------------------------------------setting1")
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'pingback.middleware.PingbackMiddleware',
    'blog.middleware.OnlineMiddleware',
    'django_pdb.middleware.PdbMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
print("----------------------------------------------------setting2")
INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'xiaojunBlog.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'xiaojunBlog.wsgi.application'

print("----------------------------------------------------setting3")

DIRECTORY_URLS = (
    'http://ping.blogs.yandex.ru/RPC2',
    'http://rpc.technorati.com/rpc/ping',
)

import os
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '..', '../blog/templates').replace('\\','/'),)
print("----------------------------------------------------settingapp")
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.markup',
    'django_xmlrpc',
    'duoshuo',
    'pingback',
    'blog',
)
print("----------------------------------------------------settingdebug")

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',

)

if DEBUG:
    INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar', )
    MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware', )
    LOG_FILE = '/tmp/blog.log'
else:
    LOG_FILE = '/home/weirdbird/virtualenvs/bloga/logs/all.log'


print("----------------------------------------------------settinglog")
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'simple': {
            'format': '[%(levelname)s] %(module)s : %(message)s'
        },
        'verbose': {
            'format': '[%(asctime)s] [%(levelname)s] %(module)s : %(message)s'
        }
    },

    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
            },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': LOG_FILE,
            'mode': 'a',
            },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false']
        }
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
            },
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
            },
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
            },
        }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'options': {
            'MAX_ENTRIES': 1024,
            }
    },
    'memcache': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/home/weirdbird/memcached.sock',
        'options': {
            'MAX_ENTRIES': 1024,
            }
    },
    }


#配置文章开头使用rst格式无显示的问题
RESTRUCTUREDTEXT_FILTER_SETTINGS = {
    'doctitle_xform': False,
    }

PAGE_NUM = 10
RECENTLY_NUM = 15
HOT_NUM = 15
ONE_DAY = 24*60*60
FIF_MIN = 15*60
FIVE_MIN = 5*60

DUOSHUO_SECRET = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
DUOSHUO_SHORT_NAME = 'xxxxxxxx'