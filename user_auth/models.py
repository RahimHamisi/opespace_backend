from django.db import models
import uuid
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    USER_CHOICES=[
        ('registered', 'Registered'), 
        ('anonymous', 'Anonymous')

    ]
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    username=models.CharField(max_length=20,null=True,blank=True,unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?255\d{9}$', 
        message="Phone number must be in the format '+255XXXXXXXXX' with 9 digits after 255"
    )
    phone_number=models.CharField(max_length=13,validators=[phone_regex],null=True,blank=True)
    is_verified=models.BooleanField(default=False)
    user_type = models.CharField(max_length=10, choices=USER_CHOICES,default='anonymous')



    def __str__(self):
        return f"{self.username if self.username else 'Anonymous'} - {self.user_type}"


  