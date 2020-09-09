import os
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'secret-key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#for photo storage on aws
AWS_ACCESS_KEY_ID = 'access-key'
AWS_SECRET_ACCESS_KEY = 'secret-key'
AWS_STORAGE_BUCKET_NAME = 'bucketname'

GOOGLE_API = 'api-key'

TIME_ZONE = ''
