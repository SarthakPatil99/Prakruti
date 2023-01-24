from django.shortcuts import render, redirect, HttpResponse
# from .models import User
from django.contrib.auth.models import User, auth
# from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.utils.datastructures import MultiValueDictKeyError
from sqlalchemy import null
import random

jinja = {}


def index(request):
    return render(request, 'index.html')


def signup(request):
    return render(request, 'signup.html')

# Login Logout Signup Password Handling


def password_check(request, passwd):

    SpecialSym = ['$', '@', '#', '%']
    val = True

    if len(passwd) < 6:
        messages.error(request, "LENGTH SHOULD BE AT LEAST 6!!!")
        val = False

    if len(passwd) > 20:
        messages.error(request, "LENGTH SHOULD NOT BE GREATER THAN 8!!!")
        val = False

    if not any(char.isdigit() for char in passwd):
        messages.error(request, "PASSWORD SHOULD HAVE AT LEAST ONE NUMERAL!!!")
        val = False

    if not any(char.isupper() for char in passwd):
        messages.error(
            request, "PASSWORD SHOULD HAVE AT LEAST ONE UPPERCASE LETTER!!!")
        val = False

    if not any(char.islower() for char in passwd):
        messages.error(
            request, "PASSWORD SHOULD HAVE AT LEAST ONE LOWERCASE LETTER!!!")
        val = False

    if not any(char in SpecialSym for char in passwd):
        messages.error(
            request, "PASSWORD SHOULD HAVE AT LEAST ONE OF THE SYMBOLS $@#!!!")
        val = False
    if val:
        return val


def handleSignUp(request):
    print('----------------------1')
    if request.method == 'POST':
        urname = request.POST['urname']
        fname = request.POST['fname']
        mname = request.POST['mname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        pwd = request.POST['pwd']
        cpwd = request.POST['confirm_pwd']
        print('-------------------------2')
        if User.objects.filter(username=urname):
            messages.error(
                request, "USERNAME ALREADY EXIST! PLEASE TRY SOME ANOTHER USERNAME")
            return redirect('/signup')

        if User.objects.filter(email=email):
            messages.error(
                request, "E-MAIL ALREADY EXIST! PLEASE TRY SOME ANOTHER E-MAIL")
            return redirect('/signup')

        if pwd != cpwd:
            messages.error(request, "PASSWARD DOES NOT MATCH!!!")
            return redirect('/signup')

        if (not password_check(request, pwd)):
            return redirect('/signup')

        if len(phone) < 10:
            messages.error(request, "INVALID PHONE NUMBER!!!")
            return redirect('/signup')

        user = User.objects.create_user(
            username=urname, password=pwd, email=email, first_name=fname, last_name=lname)
        user.save()

        messages.success(
            request, "Your account has been successfully created.")
        return redirect('/')
    else:
        return render(request, 'signup.html')


def handleLogin(request):
    print("0")
    if request.method == 'POST':
        print(request.POST)
        print("0.1")
        log_usr = request.POST['log_username']
        log_pwd = request.POST['log_pwd']
        print("0.2", log_usr)
        user = auth.authenticate(username=log_usr, password=log_pwd)
        print("0.3", user)
        if user is not None:
            Whos = User.objects.filter(username__contains=user)
            auth.login(request, user)
            messages.success(request, 'Successfully Logged In.')
            print("1")
            for Who in Whos:
                print("hihihihih")
                print(Who.is_superuser)
                if Who.is_superuser:
                    # jinja["Who"] = Who.username
                    return render(request, 'admin/Dashboard.html', jinja)
                else:
                    jinja["Who"] = ""
                    return render(request, 'index.html', jinja)
        else:
            messages.error(request, 'Invalid Credentials, Please try again.')
            return redirect('/')
    return HttpResponse('404 - Not Found')


def handleLogout(request):
    jinja["Who"] = ""
    auth.logout(request)
    messages.success(request, 'Successfully Logged Out')
    return redirect('/')


def chPass(request):
    print("0")
    if request.method == 'POST':
        print(request.POST)
        chPassMail = request.POST['chPassMail']
        conf_pass = request.POST['confPass']

        try:
            print("in try")
            # User.objects.filter(email=chPassMail).update(password=conf_pass)
            return redirect('/')
        except Exception as e:
            print('somthing wrong', e)

    return redirect('/')

# -----------------------------USER SIDE---------------------------


def home(request):
    return HttpResponse('this is home')


def analyze(request):
    return render(request, 'user/Analyzer.html')


def recommend(request):
    return render(request, 'user/Reccomender.html')


def shopping(request):
    return render(request, 'user/Shopping.html')


def U_profile(request):
    return render(request, 'user/U_profile.html', {'admin': 0})

def profileU(request):
    return render(request, 'user/U_profile.html', {'admin': 1})

# -----------------------------ADMIN SIDE---------------------------


def dashboard(request):
    return render(request, 'admin/Dashboard.html')


def patients(request):
    return render(request, 'admin/patients.html')


def appointments(request):
    return render(request, 'admin/appointments.html')


def M_remedies(request):
    return render(request, 'admin/M_remedies.html')


def H_remedies(request):
    return render(request, 'admin/H_remedies.html')


def blogs(request):
    return render(request, 'admin/blogs.html')


def orders(request):
    return render(request, 'admin/Orders.html')

def A_profile(request):
    # jinja["prof_who"] = request.user
    return render(request, 'admin/A_profile.html', {'admin': 0})

def profileA(request):
    return render(request, 'admin/A_profile.html', {'admin': 1})
