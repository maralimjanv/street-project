from django.db import models


# Create your models here.


class User(models.Model):
    chat_id = models.BigIntegerField(primary_key=True, unique=True)
    lang = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    name = models.CharField(max_length=20, null=True)
    contact = models.CharField(max_length=20, null=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return f'{self.chat_id}'


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name_uz = models.CharField(max_length=20)
    name_ru = models.CharField(max_length=20)
    name_eng = models.CharField(max_length=20)

    def __str__(self):
        return self.name_uz


class Branches(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    lat = models.CharField(max_length=30)
    lon = models.CharField(max_length=30)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.id} {self.name}'


class Items(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    caption = models.TextField()
    photo = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Basket(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    count = models.SmallIntegerField(default=1)

    def __str__(self):
        return f'{self.user}'
