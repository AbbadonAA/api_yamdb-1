from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username



ROLES = (
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )

class User(AbstractUser):
    username = models.CharField(
        validators=(validate_username,),
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default='user',
        blank=True
    )
    confirmation_code = models.CharField(
        max_length=255,
        null=True,
        blank=False,
        default='XXXX'
    )
    bio = models.TextField(
        blank=True,
    )
    first_name = models.CharField(
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        blank=True
    )
    

    @property
    def is_user(self):
        return self.role == 'user'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username
