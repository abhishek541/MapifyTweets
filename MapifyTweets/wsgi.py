"""
WSGI config for MapifyTweets project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

for k in sorted(os.environ.keys()):
    v = os.environ[k]
    print ('%-30s %s' % (k,v[:70]))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MapifyTweets.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
