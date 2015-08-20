"""
WSGI config for italiansushi_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "italiansushi_project.settings")

### local server settings ###
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

### HEROKU SERVER SETTINGS: comment out these lines to run website locally, but keep them uncommented for heroku 
from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())