from django.apps import apps
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError, NotFound
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, userInfo):
        user = self.model(
            email=userInfo['email'],
            username=userInfo['username'],
        )
        password = self.checkPassword(userInfo)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, userInfo):
        user = self.model(
            email=userInfo['email'],
            username=userInfo['username'],
            is_staff=True,
            is_superuser=True,
        )
        password = self.checkPassword(userInfo)
        user.set_password(password)
        user.save()
        return user

    def checkPassword(self, userInfo):
        password = userInfo['password']
        password2 = userInfo['password2']

        if password != password2:
            raise ValidationError(
                {'password': 'Passwords must match'})

        return password
