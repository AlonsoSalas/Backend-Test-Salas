from django.db import models
from django.contrib.auth.models import AbstractUser

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import uuid
from common.models import BaseModel
from .managers import UserManager


class CustomUser(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    objects = UserManager()
