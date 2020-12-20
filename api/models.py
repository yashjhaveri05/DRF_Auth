from django.db import models
from django.utils import timezone
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import User

class Favourite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    favourites = models.CharField(max_length=50)

    def __str__(self):
        return self.favourites