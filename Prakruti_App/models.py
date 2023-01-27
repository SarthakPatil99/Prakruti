from django.db import models

class Users(models.Model):
    UserName = models.CharField(max_length=20, default='')
    Middle_name = models.CharField(max_length=20, default='')
    Phone_No = models.BigIntegerField(default=0)
    Age = models.IntegerField(default=0)
    Gender = models.CharField(max_length=10, default='')
    P_Prakruti = models.CharField(max_length=7, default='')
    S_Prakruti = models.CharField(max_length=7, default='')
    Img = models.ImageField(null=True, blank=True, upload_to="Prakruti_App/Users_images/",
                            default="Prakruti_App/Users_images/user1.jpg")


class Appointments(models.Model):
    Day = models.DateField()
    TimeSlot = models.CharField(max_length=20, default='')
    Status = models.CharField(max_length=20, default='')
    P_med = models.CharField(max_length=20, default='')


class M_remedy(models.Model):
    Name = models.CharField(max_length=20, default='')
    Desc = models.CharField(max_length=20, default='')
    Content = models.CharField(max_length=20, default='')
    Quantity = models.IntegerField()
    Price = models.IntegerField()
    Img = models.ImageField(
        null=True, blank=True, upload_to="Prakruti_App/Med_images/",  default="Prakruti_App/Med_images/mr1.jpg")


class H_remedy(models.Model):
    Name = models.CharField(max_length=20, default='')
    Desc = models.CharField(max_length=20, default='')
    Accessories = models.CharField(max_length=20, default='')
    Img = models.ImageField(
        null=True, blank=True, upload_to="Prakruti_App/Hom_images/",  default="Prakruti_App/Hom_images/hr1.jpg")


class Blogs(models.Model):
    Title = models.CharField(max_length=20, default='')
    Type = models.CharField(max_length=20, default='')
    Content = models.CharField(max_length=20, default='')
    text = models.CharField(max_length=20, default='')
    Img = models.ImageField(
        null=True, blank=True, upload_to="Prakruti_App/blogs_images/",  default="Prakruti_App/blogs_images/blog1.jpg")
