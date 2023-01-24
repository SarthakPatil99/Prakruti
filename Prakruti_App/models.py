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


class Appointments(models.Model):
    Day = models.DateField()
    TimeSlot = models.CharField()
    Status = models.CharField()
    P_med = models.CharField()


class M_remedy(models.Model):
    Name = models.CharField()
    Desc = models.CharField()
    Content = models.CharField()
    Quantity = models.IntegerField()
    Price = models.IntegerField()
    Img = models.ImageField()


class H_remedy(models.Model):
    Name = models.CharField()
    Desc = models.CharField()
    Accessories = models.CharField()
    Img = models.ImageField()


class Blogs(models.Model):
    Title = models.CharField()
    Type = models.CharField()
    Content = models.CharField()
    text = models.CharField()
    Img = models.ImageField()
