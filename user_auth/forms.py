from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistration(UserCreationForm):
    class Meta:
        model = User
        fields = ['phone', 'first_name', 'last_name', 'email', 'gender', 'password1', 'password2'] 
