from django.db import models
from passlib.hash import pbkdf2_sha256
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=1000)
    url = models.URLField()
    picture = models.URLField()
    nutriscore = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    picture_nutrition = models.URLField()

    def __str__(self):
        return self.name


class Favorite(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)


class Substitute(models.Model):
    name =  models.CharField(max_length=250)
    url = models.URLField()
    picture = models.URLField()
    nutriscore = models.CharField(max_length=100)
    category = models.CharField(max_length=250)
    picture_nutrition = models.URLField(default='0000000')
    favorite_id = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name