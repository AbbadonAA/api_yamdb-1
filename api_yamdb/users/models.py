from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


ROLES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class RoleUser:
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class User(AbstractUser):
    username = models.CharField(
        validators=(validate_username,),
        max_length=30,
        unique=True,
    )
    email = models.EmailField(
        unique=True,
    )
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default='user',
    )
    confirmation_code = models.CharField(
        max_length=30,
        null=True,
        default='XXXX'
    )
    bio = models.TextField(
        blank=True,
    )
    first_name = models.CharField(
        max_length=30,
        blank=True
    )
    last_name = models.CharField(
        max_length=30,
        blank=True
    )

    @property
    def is_user(self):
        return self.role == RoleUser.USER

    @property
    def is_admin(self):
        return self.role == RoleUser.ADMIN

    @property
    def is_moderator(self):
        return self.role == RoleUser.MODERATOR

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username
