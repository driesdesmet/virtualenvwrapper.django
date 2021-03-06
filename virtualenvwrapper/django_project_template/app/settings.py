# Django settings for {{ project_name }} project.
import os
import socket
import re

# These must be set to True if SSL is in use
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
HOST_NAME = socket.gethostname()

DEBUG = True
TEMPLATE_DEBUG = True
THUMBNAIL_DEBUG = True

ADMINS = (
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite_database',
    }
}
TIME_ZONE = 'America/Denver'
SITE_ID = 1
USE_L10N = True
USE_TZ = True

# Set Sorl Thumbnailer to png to preserve transparent backgrounds
THUMBNAIL_FORMAT = 'PNG'

# Set the site title in Grappelli
GRAPPELLI_ADMIN_TITLE = '{{ project_name }} Admin Center'

MEDIA_ROOT = os.path.join(PROJECT_PATH, '..', 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_PATH, '..', "static")
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'public'),
)

STATICFILES_FINDERS = (
    'compressor.finders.CompressorFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

SECRET_KEY = '{{ secret_key }}'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'fusionbox.middleware.GenericTemplateFinderMiddleware',
    # 'fusionbox.middleware.RedirectFallbackMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'djangosecure.middleware.SecurityMiddleware',
)

ROOT_URLCONF = 'app.urls'

WSGI_APPLICATION = 'app.wsgi.application'
FORCE_SCRIPT_NAME = ''

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli',  # Must go before admin.
    'django.contrib.admin',

    'debug_toolbar',
    'compressor',
    'fusionbox.core',
    'south',
    'django_extensions',
    'djangosecure',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
}

SCSS_IMPORTS = (
    os.path.join(STATICFILES_DIRS[0], 'css'),
)

# django-compressor setting
COMPRESS_ENABLED = True
COMPRESS_PRECOMPILERS = (
    ('text/coffeescript', 'coffee --compile --stdio'),
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/x-sass', 'sass {infile} {outfile}'),
    ('text/x-scss', 'python -mscss {infile} -o {outfile} %s' %
     '-I ' + ' '.join(['"%s"' % d for d in SCSS_IMPORTS])
    )
)

INTERNAL_IPS = (
    '127.0.0.1',
)

EMAIL_LAYOUT = 'mail/base.html'

IGNORABLE_404_URLS = (
    re.compile(r'\.(php|cgi)$'),
    re.compile(r'/null/?$'),
    re.compile(r'^/phpmyadmin/', re.IGNORECASE),
    re.compile(r'^/favicon\.ico.*$'),
    re.compile(r'^/wp-admin/'),
    re.compile(r'^/cgi-bin/'),
    re.compile(r'^(?!/static/).*\.(css|js)/?$'),
)

# Import server specific settings 'settings_<hostname>.py'
try:
    import imp, sys
    module_name = 'settings_' + HOST_NAME
    module_info = imp.find_module(module_name, [PROJECT_PATH] + sys.path)
    live_settings = imp.load_module(module_name, *module_info)
except ImportError:
    pass
else:
    try:
        attrlist = live_settings.__all__
    except AttributeError:
        attrlist = dir(live_settings)
    for attr in attrlist:
        if attr.startswith('__'):
            continue
        globals()[attr] = getattr(live_settings, attr)

try:
    from settings_local import *
except ImportError:
    pass


DATABASE_ENGINE = DATABASES['default']['ENGINE']

# This must go _after_ the cache backends are configured, which could be in
# local settings
from django.template.loader import add_to_builtins
add_to_builtins('cachebuster.templatetags.cachebuster')

if not DEBUG:
    # if not `running in runserver` would be a better condition here
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
    )
