<<<<<<< HEAD
"""
WSGI config for crowdfunding project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crowdfunding.settings")

application = get_wsgi_application()
=======
"""
WSGI config for crowdfunding project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crowdfunding.settings")

application = get_wsgi_application()
>>>>>>> 6e1d63b04ab646ff1a8d27a8a88c948455db2318
