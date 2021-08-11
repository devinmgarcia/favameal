from django.db import models
from django.contrib.auth.models import User

class Meal(models.Model):

    name = models.CharField(max_length=55)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)
    favorite = models.ManyToManyField(User, through="FavoriteMeal", related_name="favoritemeal")

    # TODO: Add an user_rating custom properties
    @property
    def starred(self):
        return self.__starred

    @starred.setter
    def starred(self, value):
        self.__starred = value


    # TODO: Add an avg_rating custom properties
