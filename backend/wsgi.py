import os
from django.core.wsgi import get_wsgi_application

port = os.environ.get("PORT")
if port:
    os.environ["DJANGO_RUN_PORT"] = port  
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()
