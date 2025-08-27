from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField
from django.urls import reverse

# Create your models here.
GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

class User(AbstractUser):
    username = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=14, blank=True, unique=True)
    is_agent = models.BooleanField(default=False)
    gender = models.CharField(max_length=20, choices=GENDER, null=True, blank=True)
    user_id = ShortUUIDField(
        unique=True, length=6, max_length=25, prefix='DSA', alphabet='1234567890')
    image = models.ImageField(upload_to='users/', default='../media/users/newUser.jpg', null=True, blank=True)
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.first_name
    

    def avatar(self):
        if self.image:
            return self.image.url
        
    
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    
