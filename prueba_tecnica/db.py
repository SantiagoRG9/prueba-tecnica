from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent

#SQL LITE
PRO = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}