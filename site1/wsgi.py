# -*- coding: utf-8 -*-

import os
import sys
import platform

# путь к проекту
sys.path.insert(0, '/home/c/ck75028/django_7en2w/public_html')
# путь к фреймворку
sys.path.insert(0, '/home/c/ck75028/django_7en2w/public_html/site1')
# путь к виртуальному окружению
python_version = ".".join(platform.python_version_tuple()[:2])
sys.path.insert(0, '/home/c/ck75028/django_7en2w//django/lib/python{0}/site-packages'.format(python_version))
os.environ["DJANGO_SETTINGS_MODULE"] = "site1.settings"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
