import os
import django

# Configure o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quack_project.settings')
django.setup()

from quack_app.models import User

user = User.objects.get(handle="user")
user.set_password("user1234")