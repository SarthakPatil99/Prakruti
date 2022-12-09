from django.db import models


class Users(models.Model):
    UserName = models.CharField(max_length=20)
    First_name = models.CharField(max_length=20)
    Middle_name = models.CharField(max_length=20)
    Last_name = models.CharField(max_length=20)
    Password = models.CharField(max_length=20)
    Email = models.EmailField(max_length=40)
    Phone_No = models.IntegerField()
    Admin = models.BooleanField(default=False)
