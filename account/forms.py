from django.forms import ModelForm
from user_auth.models import User 


class UserUpdateForm(ModelForm):
    class Meta:
        model = User 
        fields = ['dob', 'address', 'image']