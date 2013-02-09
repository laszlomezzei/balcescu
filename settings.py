import os

"""Setting file for the Cloud SQL guestbook"""

CLOUDSQL_INSTANCE = 'iss-flasktest-shopshape'
DATABASE_NAME = 'shopshape'
USER_NAME = 'root'
PASSWORD = ''


##if (os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine') or
##    os.getenv('SETTINGS_MODE') == 'prod'):
##    print "GAE"
#    # Running on production App Engine, so use a Google Cloud SQL database.
#    DATABASES = {
#        'default': {
#            'ENGINE': 'google.appengine.ext.django.backends.rdbms',
#            'INSTANCE': 'my_project:instance1',
#            'NAME': 'my_db',
#        }
#    }
#else:
print "localhost"
# Running in development, so use a local MySQL database.
DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'root',
            'PASSWORD': PASSWORD,
            'HOST': '127.0.0.1',
            'NAME': DATABASE_NAME

        }
    }