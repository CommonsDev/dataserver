# -*- coding: utf-8 -*-
""" Django settings for dataserver project. """

from .site_settings import *  # NOQA

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-FR'

LANGUAGES = [
    ('fr-FR', 'French'),
]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

import os

PROJECT_DIR = os.path.dirname(os.path.realpath(__file__))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, '..', 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_DIR, '..', '..', 'static/')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, '..', 'static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    # 'djangular.finders.NamespacedAngularAppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'lf&3g$4$vhxyfttxs&q$9leua)7xqnebso4pyf&9i%tsgz1haf'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'userena.backends.UserenaAuthenticationBackend',
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'dataserver.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'dataserver.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates"
    # or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, '..', 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'multiuploader.context_processors.booleans',
)

INSTALLED_APPS = (
    'south',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.admin',
    'django_comments',
    'corsheaders',
    'reversion',
    'multiuploader',
    'sorl.thumbnail',
    'autoslug',
    'taggit',
    'sendfile',
    'compressor',
    'django_extensions',
    'pyelasticsearch',
    'guardian',
    'userena',
    'tastypie',
    'haystack',
    'cacheops',

    # Dataserver
    # WARNING: order matters:
    # notably scout → projects → commons (for migrations)
    #
    # 'alambic',

    'accounts',
    'bucket',
    # 'deal',
    'flipflop',
    'graffiti',
    'scout',
    'projects',
    'projectsheet',
    'projecttool',
    'graffiti',
    'commons',
    'transport_vlille',
    'unisson',

    'simple_history',

)

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
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

LEAFLET_CONFIG = {
    'TILES_URL': 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    'MINIMAP': True,
}

ANONYMOUS_USER_ID = -1
LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
# LOGIN_URL = '/login/'
LOGOUT_URL = '/accounts/signout/'

AUTH_PROFILE_MODULE = 'accounts.Profile'

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
)

# TASTYPIE/API
CORS_ORIGIN_ALLOW_ALL = True
TASTYPIE_FULL_DEBUG = DEBUG
APPEND_SLASH = False
TASTYPIE_ALLOW_MISSING_SLASH = True
TASTYPIE_DEFAULT_FORMATS = ['json']


# bucket
BUCKET_FILES_FOLDER = 'bucket'

# multiuploader
MULTIUPLOADER_FILE_EXPIRATION_TIME = 3600

MULTIUPLOADER_FORMS_SETTINGS = {
    'default': {
        'FILE_TYPES': ["txt", "zip", "jpg", "jpeg", "flv", "png"],
        'CONTENT_TYPES': [
            'image/jpeg',
            'image/png',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # NOQA
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-powerpoint',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',  # NOQA
            'application/vnd.oasis.opendocument.text',
            'application/vnd.oasis.opendocument.spreadsheet',
            'application/vnd.oasis.opendocument.presentation',
            'text/plain',
            'text/rtf',
        ],
        'MAX_FILE_SIZE': 10485760,
        'MAX_FILE_NUMBER': 5,
        'AUTO_UPLOAD': True,
    },
}

# SENDFILE
SENDFILE_BACKEND = 'sendfile.backends.development'

# SORL
# Needed for Pdf conv
THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.convert_engine.Engine'
THUMBNAIL_CONVERT = 'gm convert'
THUMBNAIL_IDENTIFY = 'gm identify'
# ———————————————————————————————————————————————————————————————————— Cacheops

DATASERVER_REDIS_CACHE_DB = os.environ.get('DATASERVER_REDIS_CACHE_DB',
                                           u'127.0.0.1:6379:2')

CACHE_HOST, CACHE_PORT, CACHE_DB_NUM = DATASERVER_REDIS_CACHE_DB.split(':', 3)

CACHEOPS_REDIS = {
    'host': CACHE_HOST,
    'port': int(CACHE_PORT),
    'db': int(CACHE_DB_NUM),
    'socket_timeout': 5,
}

# Not necessary until https://github.com/Suor/django-cacheops/pull/134 is integrated  # NOQA
CACHEOPS_USE_LOCK = False

CACHE_ONE_HOUR = 60 * 60
CACHE_ONE_DAY = CACHE_ONE_HOUR * 24
CACHE_ONE_WEEK = CACHE_ONE_DAY * 7
CACHE_ONE_MONTH = CACHE_ONE_DAY * 31

try:
    CACHEOPS

except NameError:
    CACHEOPS = {
        # Automatically cache any User.objects.get() calls
        # for 30 minutes. This includes request.user or
        # post.author access, where Post.author is a foreign
        # key to auth.User.
        'auth.user': {'ops': 'get', 'timeout': CACHE_ONE_WEEK},

        # Automatically cache all gets and queryset fetches
        # to other django.contrib.auth and oneflow.base models
        # for an hour.
        'auth.*': {'ops': ('fetch', 'get'), 'timeout': CACHE_ONE_DAY},

        # Cache gets, fetches, counts and exists to Permission
        # 'all' is just an alias for ('get', 'fetch', 'count', 'exists')
        'auth.permission': {'ops': 'all', 'timeout': CACHE_ONE_DAY},

        'contenttypes.contenttype': {'ops': 'all', 'timeout': CACHE_ONE_WEEK},

        # Everything is automatically cached for one day.
        # Override CACHEOPS in site_settings if you
        # need a more granular configuration.
        '*.*': {'ops': 'all', 'timeout': CACHE_ONE_DAY},
    }
