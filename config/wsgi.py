import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Replace 'myproject' with your project name

application = get_wsgi_application()
