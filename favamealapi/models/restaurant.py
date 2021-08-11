from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):

    name = models.CharField(max_length=55, unique=True)
    address = models.CharField(max_length=255)
    favorite = models.ManyToManyField(User, through="FavoriteRestaurant", related_name="favoriterestaurant")

    @property
    def starred(self):
        return self.__starred

    @starred.setter
    def starred(self, value):
        self.__starred = value