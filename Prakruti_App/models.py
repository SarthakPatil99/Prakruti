from django.db import models


class Users(models.Model):
    UserName = models.CharField(max_length=20, default='')
    # UserName = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Middle_name = models.CharField(max_length=20, default='')
    Phone_No = models.BigIntegerField(default=0)
    Age = models.IntegerField(default=0)
    Gender = models.CharField(max_length=10, default='')
    P_Prakruti = models.CharField(max_length=7, default='')
    S_Prakruti = models.CharField(max_length=7, default='')
    Img = models.ImageField(null=True, blank=True, upload_to="Prakruti_App/Users_images/",
                            default="Prakruti_App/Users_images/user1.jpg")


class Appointments(models.Model):
    U_id = models.BigIntegerField(default=0)
    Date = models.DateField(null=True)
    TimeSlot = models.CharField(max_length=20, default='')
    Status_A = models.BooleanField(default=False)
    Status_R = models.BooleanField(default=False)
    P_med = models.TextField(default='')


class M_remedy(models.Model):
    Name = models.CharField(max_length=20, default='')
    Desc = models.TextField(default='')
    Content = models.TextField(default='')
    Quantity = models.IntegerField(default=0)
    Price = models.IntegerField(default=0)
    Img = models.ImageField(
        null=True, blank=True, upload_to="Prakruti_App/Med_images/",  default="Prakruti_App/Med_images/mr1.jpg")


class H_remedy(models.Model):
    Name = models.CharField(max_length=20, default='')
    Desc = models.TextField(default='')
    Accessories = models.TextField(default='')
    Img = models.ImageField(
        null=True, blank=True, upload_to="Prakruti_App/Hom_images/",  default="Prakruti_App/Hom_images/hr1.jpg")


class Blogs(models.Model):
    Title = models.CharField(max_length=20, default='')
    Type = models.CharField(max_length=20, default='')
    Content = models.TextField(default='')
    Date = models.DateField(null=True)
    file = models.FileField(null=True, blank=True,
                            upload_to="Prakruti_App/Blogs/", default="Prakruti_App/Blogs/hr1.jpg")


class Orders(models.Model):
    o_id = models.IntegerField(default=0,primary_key=True)
    UserName = models.CharField(max_length=20, default='')
    Date = models.DateField()
    Time = models.TimeField()
    Status = models.BooleanField(default=False)


class Med_per_ord(models.Model):
    o_id = models.IntegerField(default=0)
    m_id = models.IntegerField(default=0)
    m_name =models.CharField(default="",max_length=100,null=True)

class Prakruti_Quetions(models.Model):
    que = models.TextField(default='')
    choice1 = models.TextField(default='')
    choice2 = models.TextField(default='')
    choice3 = models.TextField(default='')
    choice4 = models.TextField(default='')